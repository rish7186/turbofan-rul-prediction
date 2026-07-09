"""
Turbofan Engine Remaining Useful Life (RUL) Prediction

Main project entry point.
The interactive application is implemented with Streamlit
and located in app/app.py.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the Streamlit RUL prediction dashboard."""

    project_root = Path(__file__).resolve().parent
    app_path = project_root / "app" / "app.py"

    if not app_path.exists():
        print(f"Error: Streamlit application not found at: {app_path}")
        sys.exit(1)

    print("=" * 60)
    print("Turbofan Engine Remaining Useful Life Prediction")
    print("=" * 60)
    print(f"Launching application: {app_path}")
    print("Press Ctrl+C to stop the application.")
    print("=" * 60)

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(app_path)
            ],
            check=True
        )

    except KeyboardInterrupt:
        print("\nApplication stopped by user.")

    except subprocess.CalledProcessError as e:
        print(f"\nFailed to launch Streamlit application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()