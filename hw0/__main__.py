#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: hw0 {{bbox}}")
        sys.exit(1)

    if sys.argv[1] == "bbox":
        import draw_bounding_box

        sys.exit(draw_bounding_box.main())
    else:
        print(f"Unknown command: {sys.argv[1]}")
        sys.exit(1)
