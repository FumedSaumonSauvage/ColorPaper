#!/bin/bash

# Configuration
WALLPAPER_DIR="$HOME/Desktop/wp"
CURATED_DIR="$HOME/Desktop/wp/good_wp"
PLASMA_CONFIG="$HOME/.config/plasma-org.kde.plasma.desktop-appletsrc"

if [ ! -d "$CURATED_DIR" ]; then
    mkdir -p "$CURATED_DIR"
fi

# Get the current wallpaper from the configuration file
CURRENT_WALLPAPER=$(grep -oP 'Image=file://\K.*' "$PLASMA_CONFIG" | grep "$WALLPAPER_DIR")

if [ -z "$CURRENT_WALLPAPER" ]; then
    echo "Could not determine the current wallpaper from the wallpaper directory."
    exit 1
fi

case "$1" in
    "good")
        cp "$CURRENT_WALLPAPER" "$CURATED_DIR"
        echo "Wallpaper copied to $CURATED_DIR"
        ;;
    "bad")
        rm "$CURRENT_WALLPAPER"
        echo "Wallpaper deleted."
        ;;
    "")
        echo "Usage: $0 good|bad"
        exit 1
        ;;
    *)
        echo "Invalid choice. Use 'good' or 'bad'."
        exit 1
        ;;
esac

exit 0
