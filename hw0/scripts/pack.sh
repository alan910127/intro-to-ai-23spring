#/usr/bin/env bash

prefix="hw0_109652039"
target="${prefix}.zip"

zip "${target}" -j src/[a-zA-Z]*.py
zip "${target}" -j data/{output,screenshot}.png

printf "@ draw_bounding_box.py\n@=${prefix}_1.py\n" | zipnote -w "${target}"
printf "@ output.png\n@=${prefix}_1.png\n" | zipnote -w "${target}"

printf "@ remove_background.py\n@=${prefix}_2.py\n" | zipnote -w "${target}"
printf "@ screenshot.png\n@=${prefix}_2.png\n" | zipnote -w "${target}"

printf "@ data_augmentation.py\n@=${prefix}_3.py\n" | zipnote -w "${target}"
zip "${target}" "${prefix}_3.pdf"

zip "${target}" "${prefix}_4.pdf"
