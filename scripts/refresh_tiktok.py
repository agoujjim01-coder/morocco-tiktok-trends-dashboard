import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yt_dlp


CSV_PATH = Path("data/tiktok_dashboard_data.csv")
STAT_COLUMNS = ["views", "likes", "comments"]


def refresh():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH, dtype={"video_id": str})

    required = {"video_id", "url", *STAT_COLUMNS, "engagement_rate"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required CSV columns: {missing}")

    if df.empty or df["video_id"].isna().any():
        raise ValueError("Dataset contains no videos or has missing video IDs.")

    if df["video_id"].duplicated().any():
        raise ValueError("Duplicate video IDs detected. Refresh cancelled.")

    if df["url"].isna().any():
        raise ValueError("Missing video URLs detected. Refresh cancelled.")

    for column in STAT_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="raise")

        if df[column].isna().any() or (df[column] < 0).any():
            raise ValueError(f"Invalid existing statistics in {column}.")

    original = df.copy(deep=True)
    successes = 0
    failures = []

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
        "ignoreerrors": False,
        "socket_timeout": 20,
        "retries": 2,
        "extractor_retries": 2,
    }

    for index, row in df.iterrows():
        video_id = str(row["video_id"])
        url = str(row["url"])

        print(f"Refreshing video {video_id}...", flush=True)

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)

            if not isinstance(info, dict):
                raise ValueError("No metadata returned.")

            extracted_id = str(info.get("id", ""))

            if extracted_id != video_id:
                raise ValueError(
                    f"Video ID mismatch: expected {video_id}, got {extracted_id}"
                )

            fresh = {}

            for column, metadata_key in [
                ("views", "view_count"),
                ("likes", "like_count"),
                ("comments", "comment_count"),
            ]:
                value = info.get(metadata_key)

                if value is None:
                    raise ValueError(f"Missing {metadata_key}")

                value = int(value)

                if value < 0:
                    raise ValueError(f"Negative {metadata_key}")

                fresh[column] = value

            for column, value in fresh.items():
                df.at[index, column] = value

            views = fresh["views"]

            df.at[index, "engagement_rate"] = (
                (fresh["likes"] + fresh["comments"]) / views * 100
                if views > 0
                else 0.0
            )

            if "scraped_at" in df.columns:
                df.at[index, "scraped_at"] = (
                    datetime.now(timezone.utc).isoformat()
                )

            successes += 1
            print(f"  SUCCESS: {fresh}", flush=True)

        except Exception as error:
            failures.append(video_id)
            print(
                f"  FAILED: {type(error).__name__}: {error}",
                flush=True,
            )
            print("  Previous statistics preserved.", flush=True)

    print(f"\nSuccessful refreshes: {successes}/{len(df)}")
    print(f"Failed refreshes: {len(failures)}")

    if failures:
        print("Unrefreshed video IDs:", ", ".join(failures))

    if successes == 0:
        print("No successful extractions. Original CSV left untouched.")
        return

    if len(df) != len(original):
        raise ValueError("Row count changed unexpectedly.")

    if not df["video_id"].equals(original["video_id"]):
        raise ValueError("Video IDs or their order changed unexpectedly.")

    protected_columns = [
        column
        for column in original.columns
        if column not in STAT_COLUMNS + ["engagement_rate", "scraped_at"]
    ]

    for column in protected_columns:
        if not df[column].equals(original[column]):
            raise ValueError(f"Protected column changed: {column}")

    for column in STAT_COLUMNS + ["engagement_rate"]:
        values = pd.to_numeric(df[column], errors="raise")

        if values.isna().any() or (values < 0).any():
            raise ValueError(f"Invalid updated statistics: {column}")

    if df.equals(original):
        print("No data changed. Original CSV left untouched.")
        return

    # Write safely: replace the original only after the new file is ready.
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".csv",
            dir=CSV_PATH.parent,
            delete=False,
            encoding="utf-8",
            newline="",
        ) as temp_file:
            temp_path = Path(temp_file.name)
            df.to_csv(temp_file, index=False)

        # Verify the saved CSV before replacing the original.
        verified = pd.read_csv(temp_path, dtype={"video_id": str})

        if (
            len(verified) != len(original)
            or verified["video_id"].tolist()
            != original["video_id"].tolist()
        ):
            raise ValueError("Saved CSV validation failed.")

        os.replace(temp_path, CSV_PATH)
        print(f"CSV updated successfully: {CSV_PATH}")

    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


if __name__ == "__main__":
    refresh()


