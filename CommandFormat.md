# Command Format Documentation

This document provides a detailed overview of the command format used for remote control of mouse and keyboard actions. The commands are designed to be intuitive and straightforward, ensuring ease of use and implementation.

## General Format

Commands are sent as strings, structured in a comma-separated format. The general syntax is as follows:

```
<device>,<action>,<parameters>
```

- **`<device>`**: Specifies the device type (`mouse` or `keyboard`).
- **`<action>`**: Defines the action to be performed.
- **`<parameters>`**: Consists of additional details required for the action.

## Mouse Commands

Mouse commands control the mouse movement and clicks.

### Format

```
mouse,<action>,<x>,<y>
```

### Actions

1. **Move**: Moves the mouse cursor to the specified screen coordinates.
   - Format: `mouse,move,x,y`
   - Example: `mouse,move,100,150` (Moves cursor to coordinates (100, 150))
2. **Click**: Performs a mouse click.
   - Format: `mouse,click,<button>`
   - `<button>`: Either `left` or `right` for the respective mouse button.
   - Example: `mouse,click,left` (Performs a left mouse click)

## Keyboard Commands

Keyboard commands simulate keyboard operations like key press, release, and typing text.

### Format

```
keyboard,<action>,<keycode>/<text>
```

### Actions

1. **Press**: Simulates the pressing of a key.
   - Format: `keyboard,press,keycode`
   - `<keycode>`: Hexadecimal value of the key.
   - Example: `keyboard,press,1B` (Presses the 'Esc' key)
2. **Release**: Simulates the release of a key.
   - Format: `keyboard,release,keycode`
   - Example: `keyboard,release,1B` (Releases the 'Esc' key)
3. **Type**: Types a string of text.
   - Format: `keyboard,type,text`
   - `<text>`: The string to be typed.
   - Example: `keyboard,type,Hello World!` (Types "Hello World!")

## Notes

- The command string is case-sensitive, especially for the device and action fields.
- For the `keyboard,type` command, the entire text after `type,` is considered as the string to be typed.
- Ensure that the commands are formatted correctly to avoid any misinterpretation or errors in execution.

By adhering to these command formats, users can effectively control mouse and keyboard actions remotely with precision and reliability.