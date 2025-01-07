# Introduction

Trascii is a custom text editor built for creating ASCII art. Attempting to create monospaced ASCII art in a typical document proccessor leads to many issues – inconsistent spacing, spellcheck, and substitutions (e.g. `...` to `…`). Trascii aims to solve these issues by adding features specifically designed to make ASCII art easier.

The main feature of Trascii is its grid editing mode. It allows users to overwrite characters without ruining the spacing of the rest of the artwork. It also allows easy navigation between sections of the image. The editor automatically adds spaces, meaning the entire canvas is always accessible.

Trascii was created using Pygame and Python in Fall 2021.


<kbd>
 <img src=https://github.com/user-attachments/assets/74d74d7e-2253-4ab4-a181-600c2cb557e0>
</kbd>


# Usage

## Editing

Trascii includes 2 editing modes. To switch between them, press the Escape key, or click the symbol in the bottom-right.

### Text mode

![typingindicator](https://github.com/user-attachments/assets/4daa8f87-c2bf-4d53-8612-1e32f34ef5cf)

Text mode operates like a typical text editor. It is indicated by the "A" graphic. This is the only mode that allows the font to be changed outside of Courier New. Enter creates a newline and backspace works as usual. Editors must switch to grid mode to navigate using the arrow keys or mouse. A special command is CTRL+SPACE which allows the user to specify an amount of spaces to add.

### Grid mode

![editindicator](https://github.com/user-attachments/assets/f03418b9-250b-418b-a959-6ca900370d8e)

In grid mode, characters are overwritten instead of displaced. It is indicated by the pencil writing graphic. The grid can be navigated by clicking anywhere on the screen, or using the arrow keys. Backspace only overwrites the selected character.


## File management

Trascii has a custom file format (.trascii) which contains the text of an artwork, along with information for some settings, like the path of the background image. Trascii supports opening .txt and .trascii files, but it can be overidden to treat .txt-like files as .txt files. These are the options availible under the "File" ribbon:

<kbd>
 <img src=https://github.com/user-attachments/assets/0da990ff-ec9f-4a99-b8f6-02aa9db958ef>ft
</kbd>

"Save" creates a .trascii file of the project, "Open" opens a .txt or .trascii file, and "Export" creates a .txt file. "Charset" can be used to specify which characters are allowed in the program. The options are printable ASCII characters (the recommended default), only printable characters, only ASCII characters, and no restrictions. The latter is not recommended, since it breaks backspacing. 

## Images

Trascii allows images to be placed behind art for tracing. 

<kbd>
 <img src=https://github.com/user-attachments/assets/4e87be5d-f8e0-4c43-b4ca-5f783b9bfc71>
</kbd>

The permissible file formats are .png, .jpg, .gif, or .bmp. The image can be resized, offset from the top-left, and made opaque.

## Font

Trascii also allows the font to be adjusted.

<kbd>
 <img src=https://github.com/user-attachments/assets/65fe5a37-53c3-454b-bc71-fabef8fc43d4>
</kbd>

Users can edit the font size, line spacing, and font face. Note that grid mode must use the font Courier New, and will not load in a different font. The font size can also be adjusted using CTRL+ and CTRL-. 

# Installation

Trascii uses the packages `pygame` and `easygui`. They must be installed first. Make sure the latest version of Python is installed.

`pip install pygame`

`pip install easygui`

`git clone https://github.com/shaan-s/Trascii`

Then run `textedit.py`.
