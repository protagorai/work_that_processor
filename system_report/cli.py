from .gather import gather_all
from .save import save_report


def main():
    data = gather_all()
    path = save_report(data)
    print(f"Report saved to {path}")


if __name__ == "__main__":  # pragma: no cover
    main()
