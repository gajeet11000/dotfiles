import os
import subprocess
from typing import List
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import (
    Click,
    Drag,
    Group,
    Key,
    Match,
    Screen,
    Rule,
    ScratchPad,
    DropDown,
)
from libqtile.lazy import lazy

from user_variables import *

########################CUSTOM FUNCTIONS#################################


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def minimize_all(qtile):
    for win in qtile.current_group.windows[:]:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


def isNotMasterWindow(window):
    return window.info()["x"] != 8 and window.info()["y"] != 8


def minimize_others(qtile):
    focused_window = qtile.current_window

    current_group = qtile.current_group
    current_group_windows = current_group.windows[:]

    restore_group = qtile.groups[int(current_group.name) - 1 + 5]
    restore_group_windows = restore_group.windows[:]

    no_of_windows = len(current_group_windows)

    if (no_of_windows == 0 or no_of_windows == 1) or (
        no_of_windows == 2 and isNotMasterWindow(focused_window)
    ):
        for win in restore_group_windows:
            win.togroup(current_group.name)

    else:
        for win in current_group_windows:
            if (
                win != focused_window
                and isNotMasterWindow(win)
                and isNotMasterWindow(focused_window)
            ):
                win.togroup(restore_group.name)


def toggle_current_minimized_groups(qtile):
    current_group_index = int(qtile.current_group.name) - 1

    print(current_group_index)

    if current_group_index < 5:
        qtile.current_screen.toggle_group(qtile.groups[current_group_index + 5].name)
    else:
        qtile.current_screen.toggle_group(qtile.groups[current_group_index - 5].name)


def killall_windows(group):
    window_list = group.windows[:]
    for win in window_list:
        win.kill()


def clear_minimized_group(qtile):
    current_group_index = int(qtile.current_group.name) - 1
    killall_windows(qtile.groups[current_group_index + 5])


def clear_current_group(qtile):
    killall_windows(qtile.groups[int(qtile.current_group.name - 1)])


def maximize_by_switching_layout(qtile):
    current_layout = qtile.current_group.layout.name

    no_of_windows = len(qtile.current_group.windows[:])

    if no_of_windows > 1:
        if current_layout == "monadtall":
            qtile.current_group.layout = "max"
        elif current_layout == "max":
            qtile.current_group.layout = "monadtall"


def toggle_window_original_restore(qtile):
    current_group_index = int(qtile.current_group.name) - 1
    focused_window = qtile.current_window

    if current_group_index < 5:
        focused_window.togroup(qtile.groups[current_group_index + 5].name)
    else:
        focused_window.togroup(qtile.groups[current_group_index - 5].name)


def get_main_pane(qtile):
    windows = qtile.current_group.windows[:]
    for win in windows:
        if not isNotMasterWindow(win):
            return win


@lazy.function
def resize_window(qtile, key):
    focused_window = qtile.current_window
    is_master = not isNotMasterWindow(focused_window)

    current_layout = qtile.current_group.layout

    if current_layout.name == "monadtall":
        if is_master:
            if key == "h":
                current_layout.shrink()
            elif key == "l":
                current_layout.grow()
        else:
            if key == "j":
                current_layout.grow()
            elif key == "k":
                current_layout.shrink()
            elif key == "h":
                current_layout.shrink_main()
            else:
                current_layout.grow_main()
    elif current_layout.name == "monadwide":
        if is_master:
            if key == "k":
                current_layout.shrink()
            elif key == "j":
                current_layout.grow()
        else:
            if key == "h":
                current_layout.grow()
            elif key == "l":
                current_layout.shrink()
            elif key == "j":
                current_layout.shrink_main()
            else:
                current_layout.grow_main()


def custom_next_group(qtile):
    current_group_index = int(qtile.current_group.name) - 1
    i = current_group_index + 1

    # if its -1 then it means it's acutal index is 9
    if current_group_index == -1:
        current_group_index = 9
        # so the next index starts from 0
        i = 0

    total_groups = 10
    while i != current_group_index:
        if i < total_groups:
            if len(qtile.groups[i].windows[:]) != 0:
                if i == 9:
                    qtile.current_screen.toggle_group("0")
                else:
                    qtile.current_screen.toggle_group(str(i + 1))
                break
            i += 1
        else:
            i = 0


def custom_prev_group(qtile):
    current_group_index = int(qtile.current_group.name) - 1

    # previous group index
    i = current_group_index - 1

    # if its -1 then it means it's acutal index is 9
    if current_group_index == -1:
        current_group_index = 9
        # so the previous index is 8
        i = 8

    while i != current_group_index:
        if i >= 0:
            if len(qtile.groups[i].windows[:]) != 0:
                if i == 9:
                    qtile.current_screen.toggle_group("0")
                else:
                    qtile.current_screen.toggle_group(str(i + 1))
                break
            i -= 1
        else:
            i = 9


def regular_custom_next_group(qtile):
    current_group_no = int(qtile.current_group.name)
    if current_group_no == 0:
        qtile.current_screen.toggle_group("1")
    else:
        qtile.current_screen.next_group()


def regular_custom_prev_group(qtile):
    current_group_no = int(qtile.current_group.name)
    if current_group_no == 1:
        qtile.current_screen.toggle_group("0")
    else:
        qtile.current_screen.prev_group()


def is_app_not_open(qtile, group_name, wm_class):
    group = qtile.groups_map[group_name]
    for win in group.windows[:]:
        if wm_class in win.get_wm_class():
            return False
    return True


prev_group_save = None


def toggle_spo_group(qtile):
    global prev_group_save
    current_group = qtile.current_group

    if current_group.name == "spo":
        qtile.current_screen.toggle_group(prev_group_save)
    else:
        qtile.current_screen.toggle_group("spo")
        if is_app_not_open(qtile, "spo", "open.spotify.com"):
            qtile.spawn("brave --app=https://open.spotify.com")

    if current_group.name not in ["wa", "spo"]:
        prev_group_save = current_group.name


def toggle_wa_group(qtile):
    global prev_group_save
    current_group = qtile.current_group

    if current_group.name == "wa":
        qtile.current_screen.toggle_group(prev_group_save)
    else:
        qtile.current_screen.toggle_group("wa")
        if is_app_not_open(qtile, "wa", "web.whatsapp.com"):
            qtile.spawn("brave --app=https://web.whatsapp.com")

    if current_group.name not in ["wa", "spo"]:
        prev_group_save = current_group.name


def float_to_front(qtile):
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.bring_to_front()


def switch_max_to_monadtall(qtile):
    layout_name = qtile.current_layout.name

    if layout_name == "max":
        qtile.current_group.layout = "monadtall"


################################################################################################
####################################SHORTCUTS KEYBINDINGS#######################################


keys = [
    #################################CUSTOM FUNCTION########################################
    Key([mod, "shift"], "f", lazy.function(float_to_front)),
    Key([mod, "mod1"], "p", lazy.function(toggle_wa_group)),
    Key([mod, "mod1"], "space", lazy.function(toggle_spo_group)),
    Key(
        [mod, "mod1"],
        "f",
        lazy.function(maximize_by_switching_layout),
        desc="toggle maximize",
    ),
    Key([mod], "t", lazy.function(toggle_current_minimized_groups)),
    Key(
        [mod],
        "u",
        lazy.function(minimize_others),
        desc="Minimize all except master and focused window",
    ),
    Key(
        [mod, "shift"],
        "u",
        lazy.function(clear_minimized_group),
        lazy.function(minimize_others),
        desc="clear group then minimize there",
    ),
    Key(
        [mod],
        "r",
        lazy.function(toggle_window_original_restore),
        desc="send window to restore to original and vice-versa",
    ),
    Key([mod], "d", lazy.function(minimize_all), desc="Toggle minimization"),
    ######################################SCRIPTS###########################################
    Key(
        [mod, "shift"],
        "q",
        lazy.spawn(
            "rofi -show power-menu -modi power-menu:"
            + home + "/.config/rofi/scripts/rofi-power-menu.sh"
        ),
    ),
    Key(
        [mod],
        "s",
        lazy.spawn(
            "rofi -show Home -config "
            + home
            + "/.config/rofi/themes/search-config.rasi"
        ),
    ),
    Key(
        [mod, "shift"],
        "s",
        lazy.spawn(
            "rofi -show Home -config "
            + home
            + "/.config/rofi/themes/open-terminal-config.rasi"
        ),
    ),
    Key(
        ["mod1"],
        "space",
        lazy.spawn("bash " + home + "/.config/rofi/scripts/rofi-web-search.sh"),
    ),
    Key(
        [mod, "mod1"],
        "b",
        lazy.spawn("bash " + home + "/.config/rofi/scripts/rofi-set-bg.sh"),
    ),
    #########################################APPLICATIONS#######################################
    Key([mod], "e", lazy.spawn(file_manager)),
    Key([mod], "space", lazy.spawn("rofi -sort -sorting-method fzf -show drun")),
    Key([mod2, "mod1"], "d", lazy.spawn(file_manager + " Downloads")),
    Key([mod], "Escape", lazy.spawn("xkill")),
    Key([mod], "Return", lazy.spawn(terminal)),
    # Key([mod], "p", lazy.spawn("/usr/bin/octopi")),
    Key([mod], "a", lazy.spawn(file_manager + " /mnt/" + storage_drive)),
    Key([mod], "f", lazy.spawn(WebBrowser)),
    # Key([mod1, "shift"], "Escape", lazy.spawn("")),
    Key([], "Print", lazy.spawn("flameshot gui")),
    ##########################################SYSTEM##############################################
    # INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +5%")),
    Key([mod], "x", lazy.spawn("brightnessctl s +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-")),
    Key([mod], "z", lazy.spawn("brightnessctl s 5%-")),
    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    Key([mod], "m", lazy.spawn("amixer -q set Master toggle")),
    Key([mod], "semicolon", lazy.spawn("amixer -q set Master 5%-")),
    Key([mod], "apostrophe", lazy.spawn("amixer -q set Master 5%+")),
    # MEDIA PLAYER CONTROL
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    ##########################################WINDOW MANAGING######################################
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Window resizing
    Key([mod, "control"], "h", resize_window("h")),
    Key([mod, "control"], "l", resize_window("l")),
    Key([mod, "control"], "j", resize_window("j")),
    Key([mod, "control"], "k", resize_window("k")),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "n", lazy.layout.reset(), desc="Reset all window sizes"),
    # Toggle between different layouts as defined below
    Key(["mod1"], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, mod2], "r", lazy.reload_config(), desc="Reload the config"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "c", lazy.window.kill()),
    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    # TOGGLE NEXT AND PREVIOUS WORKSPACE
    Key([mod], "comma", lazy.function(custom_prev_group)),
    Key([mod], "period", lazy.function(custom_next_group)),
    Key([mod, "shift"], "comma", lazy.function(regular_custom_prev_group)),
    Key([mod, "shift"], "period", lazy.function(regular_custom_next_group)),
    # TOGGLE HIDDEN WORKSPACES
]
#####################################SETTING UP GROUPS###################################

group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]
group_labels = ["➊", "➋", "➌", "➍", "➎", "α", "β", "γ", "δ", "ε"]

group_layouts = [
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "bsp",
    "bsp",
    "bsp",
    "bsp",
    "bsp",
]

groups = []

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # CHANGE WORKSPACES
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                lazy.group[i.name].toscreen(),
            ),
        ]
    )

hidden_groups = [
    Group(
        name="spo",
        layout="monadtall".lower(),
        label="",
    ),
    Group(
        name="wa",
        layout="monadtall".lower(),
        label="",
    ),
]

for i in hidden_groups:
    groups.append(i)

dropdowns = [
    DropDown("term", terminal, width=0.9, height=0.9, x=0.05, y=0.05, opacity=1),
    DropDown(
        "octopi", "/usr/bin/octopi", width=0.9, height=0.9, x=0.05, y=0.05, opacity=1
    ),
    # DropDown(
    #     "spotify",
    #     ["chromium", "--app=https://open.spotify.com"],
    #     width=0.9,
    #     height=0.9,
    #     x=0.05,
    #     y=0.05,
    #     opacity=1,
    # ),
    # DropDown(
    #     "whatsapp",
    #     [WebBrowser, "--app=https://web.whatsapp.com"],
    #     width=0.9,
    #     height=0.9,
    #     x=0.05,
    #     y=0.05,
    #     opacity=1,
    # ),
]

for i in dropdowns:
    i.floating = True

# ScratchPads
groups.append(
    ScratchPad("scratchpad", dropdowns),
)


keys.extend(
    [
        Key([mod, "mod1"], "v", lazy.group["scratchpad"].dropdown_toggle("term")),
        # Key([mod, "mod1"], "p", lazy.group["scratchpad"].dropdown_toggle("whatsapp")),
        # Key(["mod1"], "space", lazy.group["scratchpad"].dropdown_toggle("spotify")),
        Key([mod], "p", lazy.group["scratchpad"].dropdown_toggle("octopi")),
    ]
)


def init_layout_theme():
    return {
        "margin": 8,
        "border_width": 2,
        "border_focus": "#E0B0FF",
        "border_normal": "#000000",
    }


layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(
        margin=8, border_width=4, border_focus="#E0B0FF", border_normal="#000000"
    ),
    layout.MonadWide(
        margin=8, border_width=4, border_focus="#E0B0FF", border_normal="#000000"
    ),
    layout.Max(
        margin=8, border_width=4, border_focus="#E0B0FF", border_normal="#000000"
    ),
    layout.Zoomy(
        margin=8, border_width=4, border_focus="#E0B0FF", border_normal="#000000"
    ),
    layout.Bsp(
        margin=8, border_width=4, border_focus="#E0B0FF", border_normal="#000000"
    ),
    layout.Floating(
        margin=8, border_width=4, border_focus="#E0B0FF", border_normal="#000000"
    ),
]

###########################################WIDGET AND BAR CONFIG######################################

# COLORS FOR THE BAR


def init_colors():
    return [
        ["#2F343F", "#2F343F"],  # color 0
        ["#2F343F", "#2F343F"],  # color 1
        ["#c0c5ce", "#c0c5ce"],  # color 2
        ["#ff5555", "#ff5555"],  # color 3
        ["#f4c2c2", "#f4c2c2"],  # color 4
        ["#ffffff", "#ffffff"],  # color 5
        ["#ffd47e", "#ffd47e"],  # color 6
        ["#62FF00", "#62FF00"],  # color 7
        ["#000000", "#000000"],  # color 8
        ["#c40234", "#c40234"],  # color 9
        ["#6790eb", "#6790eb"],  # color 10
        ["#ff00ff", "#ff00ff"],  # 11
        ["#4c566a", "#4c566a"],  # 12
        ["#282c34", "#282c34"],  # 13
        ["#212121", "#212121"],  # 14
        ["#e75480", "#e75480"],  # 15
        ["#2aa899", "#2aa899"],  # 16
        ["#abb2bf", "#abb2bf"],  # color 17
        ["#81a1c1", "#81a1c1"],  # 18
        ["#56b6c2", "#56b6c2"],  # 19
        ["#b48ead", "#b48ead"],  # 20
        ["#e06c75", "#e06c75"],  # 21
        ["#ff79c6", "#ff79c6"],  # 22
        ["#ffb86c", "#ffb86c"],
    ]  # 23


colors = init_colors()


def base(fg="text", bg="dark"):
    return {"foreground": colors[14], "background": colors[15]}


# WIDGETS FOR THE BAR


def init_widgets_defaults():
    return dict(font="Noto Sans", fontsize=16, padding=2, background=colors[1])


widget_defaults = init_widgets_defaults()

screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.Spacer(
                #     length=15,
                #     background="#282738",
                # ),
                # widget.Image(
                #     filename="~/.config/qtile/Assets/launch_Icon.png",
                #     margin=2,
                #     background="#282738",
                #     mouse_callbacks={"Button1": power},
                # ),
                # widget.Image(
                #     filename="~/.config/qtile/Assets/6.png",
                # ),
                widget.GroupBox(
                    font="FontAwesome Regular",
                    fontsize=24,
                    borderwidth=3,
                    highlight_method="block",
                    active="#E0B0FF",
                    block_highlight_text_color="#00ff00",
                    highlight_color="#4B427E",
                    inactive="#282738",
                    foreground="#4B427E",
                    background="#353446",
                    this_current_screen_border="#353446",
                    this_screen_border="#353446",
                    other_current_screen_border="#353446",
                    other_screen_border="#353446",
                    urgent_border="#353446",
                    rounded=True,
                    disable_drag=True,
                ),
                widget.Spacer(
                    length=8,
                    background="#353446",
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/1.png",
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/layout.png", background="#353446"
                ),
                widget.CurrentLayout(
                    background="#353446",
                    foreground="#E0B0FF",
                    fmt="{}",
                    font="JetBrains Bold",
                    fontsize=14,
                ),
                # widget.Image(
                #     filename="~/.config/qtile/Assets/5.png",
                # ),
                # widget.Image(
                #     filename="~/.config/qtile/Assets/search.png",
                #     margin=2,
                #     background="#282738",
                #     mouse_callbacks={"Button1": search},
                # ),
                # widget.TextBox(
                #     fmt="Search",
                #     background="#282738",
                #     font="JetBrains Mono Bold",
                #     fontsize=13,
                #     foreground="#E0B0FF",
                #     mouse_callbacks={"Button1": search},
                # ),
                # widget.Image(
                #     filename="~/.config/qtile/Assets/4.png",
                # ),
                widget.Image(
                    filename="~/.config/qtile/Assets/1.png",
                ),
                widget.WindowName(
                    background="#353446",
                    format="{name}",
                    font="JetBrains Bold",
                    foreground="#E0B0FF",
                    empty_group_string="Desktop",
                    fontsize=14,
                ),
                # widget.Image(
                #     filename="~/.config/qtile/Assets/Drop1.png",
                # ),
                widget.Image(
                    filename="~/.config/qtile/Assets/3.png",
                ),
                widget.Net(
                    font="JetBrains Bold",
                    format="  {down:.1f}{down_suffix}        {up:.1f}{up_suffix}  ",
                    background="#282738",
                    foreground="#E0B0FF",
                    # prefix="k",
                    fontsize=16,
                ),
                # widget.Image(
                #     filename="~/.config/qtile/Assets/6.png",
                #     background="#353446",
                # ),
                widget.Image(
                    filename="~/.config/qtile/Assets/9.png",
                    background="#E0B0FF",
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/8.png",
                    background="#E0B0FF",
                ),
                widget.Systray(
                    background="#282738",
                    icon_size=22,
                    padding=5,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/6.png",
                    background="#353446",
                ),
                # widget.Spacer(
                #     length=8,
                #     background="#353446",
                # ),
                widget.Image(
                    filename="~/.config/qtile/Assets/Misc/ram.png",
                    background="#353446",
                ),
                widget.Spacer(
                    length=-7,
                    background="#353446",
                ),
                widget.Memory(
                    background="#353446",
                    format="{MemUsed: .0f}{mm}",
                    foreground="#E0B0FF",
                    font="JetBrains Bold",
                    fontsize=16,
                    update_interval=1,
                ),
                # widget.Image(
                # filename='~/.config/qtile/Assets/Drop2.png',
                # ),
                widget.Image(
                    filename="~/.config/qtile/Assets/2.png",
                ),
                widget.Spacer(
                    length=8,
                    background="#353446",
                ),
                widget.BatteryIcon(
                    theme_path="~/.config/qtile/Assets/Battery/",
                    background="#353446",
                    scale=1,
                ),
                widget.Battery(
                    font="JetBrains Bold",
                    background="#353446",
                    foreground="#E0B0FF",
                    format="{percent:2.0%}",
                    fontsize=16,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/2.png",
                ),
                widget.Spacer(
                    length=8,
                    background="#353446",
                ),
                widget.Volume(
                    font="JetBrains Bold",
                    theme_path="~/.config/qtile/Assets/Volume/",
                    emoji=True,
                    fontsize=16,
                    background="#353446",
                ),
                widget.Spacer(
                    length=-5,
                    background="#353446",
                ),
                widget.Volume(
                    font="JetBrains Bold",
                    background="#353446",
                    foreground="#E0B0FF",
                    fontsize=16,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/5.png",
                    background="#353446",
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/Misc/clock.png",
                    background="#282738",
                    margin_y=6,
                    margin_x=5,
                ),
                widget.Clock(
                    format="%a, %b %d-%m-%Y %H:%M:%S",
                    background="#282738",
                    foreground="#E0B0FF",
                    font="JetBrains Bold",
                    fontsize=16,
                ),
            ],
            30,
            border_color="#282738",
        ),
    ),
]

# MOUSE CONFIGURATION
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Drag(
        [mod], "Button1", lazy.window.set_position(), start=lazy.window.get_position()
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #########################################################
#     ################ assgin apps to groups ##################
#     #########################################################
#     d["1"] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d["2"] = [ "Atom", "Subl3", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl3", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d["3"] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d["4"] = ["Gimp", "gimp" ]
#     d["5"] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d["6"] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d["7"] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d["8"] = ["pcmanfm", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "pcmanfm", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d["9"] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d["0"] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ##########################################################
#     wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen()

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME

main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh", wallpapers_path, lockscreen_wallpaper_path])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True
    switch_max_to_monadtall(qtile)


@hook.subscribe.client_killed
def check_windows_in_max_mode(window):
    switch_max_to_monadtall(qtile)


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = "floating_only"
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_width=4,
    border_focus="#E0B0FF",
    border_normal="#000000",
    fullscreen_border_width=0,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="protonvpn"),
        Match(wm_class="Arandr"),
        Match(wm_class="feh"),
        Match(wm_class="blueman-manager"),
        Match(wm_class="gnome-calculator"),
        Match(wm_class="Galculator"),
        Match(title="branchdialog"),
        Match(title="Open File"),
        Match(title="pinentry"),
        Match(title="Bitwarden"),
        Match(wm_class="ssh-askpass"),
        Match(wm_class="lxpolkit"),
        Match(wm_class="Lxpolkit"),
        Match(wm_class="yad"),
        Match(wm_class="Yad"),
        Match(wm_class="Cairo-dock"),
        Match(wm_class="cairo-dock"),
        Match(wm_class="megasync"),
        Match(wm_class="copyq"),
    ],
)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart or focus

wmname = "LG3D"
