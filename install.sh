#!/bin/bash

DOTFILES=$(dirname "$(realpath -s "$0")")
CONFIG=${CONFIG:-"$HOME/.config"}

dotfile() {
    SOURCE=$1
    TARGET=$2

    # Move dir here if it doesn't exist (should only happen when adding lines below)
    if [[ ! -e "$SOURCE" ]]; then
        mv "$TARGET" "$SOURCE"
        echo "$SOURCE does not exist, copying from $TARGET"
    fi

    # Move old file/dir if needed
    if [[ -e "$TARGET" && ! -h "$TARGET" ]]; then
        if [[ -e "$TARGET.old" ]]; then
            rm -rf "$TARGET.old"
        fi
        mv "$TARGET" "$TARGET.old"
        echo "$TARGET exists, moving to $TARGET.old"
    fi

    # Create symlink if it doesn't already exist
    if [[ ! -e "$TARGET" && ! -d "$TARGET" ]]; then
        ln -s "$SOURCE" "$TARGET"
        echo "Created symlink $SOURCE -> $TARGET"
        echo
    fi
}

#        File in repo                    File on disk
dotfile "$DOTFILES/.p10k.zsh"           "$HOME/.p10k.zsh"
dotfile "$DOTFILES/.zshrc"              "$HOME/.zshrc"
dotfile "$DOTFILES/config/alacritty"    "$CONFIG/alacritty"
dotfile "$DOTFILES/config/i3"           "$CONFIG/i3"
dotfile "$DOTFILES/config/picom"        "$CONFIG/picom"
dotfile "$DOTFILES/config/rofi"         "$CONFIG/rofi"
dotfile "$DOTFILES/config/eww"          "$CONFIG/eww"

echo "Done!"
