import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
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
from libqtile.command import lazy


# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser("~")


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


@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


def isNotMasterWindow(window):
    return window.info()["x"] != 8 and window.info()["y"] != 8


@lazy.function
def minimize_others(qtile):
    stack = qtile.current_group.windows
    current_win = qtile.current_window
    for win in stack:
        if (
            hasattr(win, "toggle_minimize")
            and win != current_win
            and isNotMasterWindow(win)
            and isNotMasterWindow(current_win)
        ):
            win.toggle_minimize()


@lazy.function
def toggleMaximize(qtile):
    qtile.current_window.toggle_maximize()


myTerm = "alacritty"  # My terminal of choice


keys = [
    # SUPER + FUNCTION KEYS
    Key(
        [mod],
        "u",
        minimize_others(),
        desc="Minimize all except master and focused window",
    ),
    Key(
        [mod, "shift"],
        "q",
        lazy.spawn(
            "rofi -show power-menu -modi power-menu:~/.config/rofi/rofi-power-menu.sh"
        ),
    ),
    Key([mod, "mod1"], "f", toggleMaximize()),
    Key([mod], "c", lazy.window.kill()),
    Key([mod], "d", minimize_all(), desc="Toggle minimization"),
    # Key([mod], "d", lazy.spawn('nwggrid -p -o 0.4')),
    Key([mod], "Escape", lazy.spawn("xkill")),
    Key([mod2, "mod1"], "d", lazy.spawn("dolphin Downloads")),
    Key([mod, "mod1"], "v", lazy.spawn(myTerm)),
    #   Key([mod], "KP_Enter", lazy.spawn('alacritty')),
    #   Key([mod], "x", lazy.shutdown()),
    # SUPER + SHIFT KEYS
    Key([mod], "e", lazy.spawn("thunar")),
    # Key([mod, "shift"], "d", lazy.spawn("dmenu_run -i -nb '#191919' -nf '#ff1493' -sb '#ff1493' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=15'")),
    #   Key([mod, "shift"], "d", lazy.spawn(home + '/.config/qtile/scripts/dmenu.sh')),
    #   Key([mod, "shift"], "q", lazy.window.kill()),
    #   Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "control"], "r", lazy.restart()),
    #   Key([mod, "shift"], "x", lazy.shutdown()),
    # CONTROL + ALT KEYS
    Key(
        ["mod1", "control"],
        "o",
        lazy.spawn(home + "/.config/qtile/scripts/picom-toggle.sh"),
    ),
    #   Key(["mod1", "control"], "t", lazy.spawn('xterm')),
    #   Key(["mod1", "control"], "u", lazy.spawn('pavucontrol')),
    # ALT + ... KEYS
    Key([mod], "p", lazy.spawn("pamac-manager")),
    Key([mod], "a", lazy.spawn("thunar /mnt/Ajeet")),
    #   Key(["mod1"], "f", lazy.spawn('firedragon')),
    Key([mod], "f", lazy.spawn("brave")),
    #   Key(["mod1"], "m", lazy.spawn('pcmanfm')),
    Key(["mod1"], "w", lazy.spawn("garuda-welcome")),
    # CONTROL + SHIFT KEYS
    Key([mod2, "shift"], "Escape", lazy.spawn("lxtask")),
    # SCREENSHOTS
    Key([], "Print", lazy.spawn("flameshot gui")),
    Key(["shift"], "Print", lazy.spawn("flameshot full -p " + home + "/Pictures")),
    #    Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),
    # MULTIMEDIA KEYS
    # INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +5%")),
    Key([mod], "x", lazy.spawn("brightnessctl s +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%- ")),
    Key([mod], "z", lazy.spawn("brightnessctl s 5%- ")),
    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    Key([mod], "m", lazy.spawn("amixer -q set Master toggle")),
    Key([mod], "semicolon", lazy.spawn("amixer -q set Master 5%-")),
    Key([mod], "apostrophe", lazy.spawn("amixer -q set Master 5%+")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    #    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    #    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    #    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
    #    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),
    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.spawn("rofi -show drun")),
    Key(["mod1"], "tab", lazy.next_layout()),
    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),
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
    ### Treetab controls
    Key(
        [mod, "control"],
        "k",
        lazy.layout.section_up(),
        desc="Move up a section in treetab",
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.section_down(),
        desc="Move down a section in treetab",
    ),
    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
]

groups = []

# FOR QWERTY KEYBOARDS
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

# FOR AZERTY KEYBOARDS
# group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

# group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
group_labels = [
    "󰏃",
    "󰏃",
    "󰏃",
    "󰏃",
    "󰏃",
    "󰏃",
    "󰏃",
    "󰏃",
    "󰏃",
    "󰏃",
]
# group_labels = ["", "", "", "", "",]
# group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = [
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "treetab",
    "floating",
]
# group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

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
            Key([mod], "Tab", lazy.screen.next_group()),
            Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
            # Key(["mod1"], "Tab", lazy.screen.next_group()),
            # Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                lazy.group[i.name].toscreen(),
            ),
        ]
    )


def init_layout_theme():
    return {
        "margin": 8,
        "border_width": 2,
        "border_focus": "#ff00ff",
        "border_normal": "#f4c2c2",
    }


layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(
        margin=8, border_width=4, border_focus="#66ff00", border_normal="#000000"
    ),
    layout.MonadWide(
        margin=8, border_width=2, border_focus="#ff00ff", border_normal="#f4c2c2"
    ),
    layout.Matrix(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Stack(**layout_theme),
    layout.Tile(**layout_theme),
    layout.TreeTab(
        sections=["FIRST", "SECOND"],
        bg_color="#141414",
        active_bg="#0000ff",
        inactive_bg="#1e90ff",
        padding_y=5,
        section_top=10,
        panel_width=280,
    ),
    layout.VerticalTile(**layout_theme),
    layout.Zoomy(**layout_theme),
]

# ScratchPads
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "term", "alacritty", width=0.8, height=0.7, x=0.1, y=0.1, opacity=1
            ),
            DropDown(
                "music",
                "alacritty -e mocp",
                width=0.90,
                height=0.5,
                x=0.05,
                y=0.0,
                opacity=0.8,
                on_focus_lost_hide=False,
            ),
        ],
    )
)

# Extend keys for scratchPad
keys.extend(
    [
        Key(["control"], "Return", lazy.group["scratchpad"].dropdown_toggle("term")),
        Key(["mod1"], "space", lazy.group["scratchpad"].dropdown_toggle("music")),
    ]
)


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
    return dict(font="Noto Sans", fontsize=9, padding=2, background=colors[1])


widget_defaults = init_widgets_defaults()


def search():
    qtile.cmd_spawn("rofi -show drun")


def power():
    qtile.cmd_spawn("sh -c ~/.config/rofi/scripts/power")


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
                    fontsize=24,
                    borderwidth=3,
                    highlight_method="block",
                    active="#CAA9E0",
                    block_highlight_text_color="#91B1F0",
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
                    foreground="#CAA9E0",
                    fmt="{}",
                    font="JetBrains Mono Bold",
                    fontsize=13,
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
                #     foreground="#CAA9E0",
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
                    font="JetBrains Mono Bold",
                    foreground="#CAA9E0",
                    empty_group_string="Desktop",
                    fontsize=13,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/3.png",
                ),
                widget.Systray(
                    background="#282738",
                    fontsize=2,
                ),
                widget.TextBox(
                    text=" ",
                    background="#282738",
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/6.png",
                    background="#353446",
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/Drop1.png",
                ),
                widget.Net(
                    format=" {down}   {up} ",
                    background="#353446",
                    foreground="#CAA9E0",
                    font="JetBrains Mono Bold",
                    # prefix="k",
                    fontsize=15,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/2.png",
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
                    foreground="#CAA9E0",
                    font="JetBrains Mono Bold",
                    fontsize=15,
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
                    font="JetBrains Mono Bold",
                    background="#353446",
                    foreground="#CAA9E0",
                    format="{percent:2.0%}",
                    fontsize=15,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/2.png",
                ),
                widget.Spacer(
                    length=8,
                    background="#353446",
                ),
                widget.Volume(
                    font="JetBrainsMono Nerd Font",
                    theme_path="~/.config/qtile/Assets/Volume/",
                    emoji=True,
                    fontsize=13,
                    background="#353446",
                ),
                widget.Spacer(
                    length=-5,
                    background="#353446",
                ),
                widget.Volume(
                    font="JetBrains Mono Bold",
                    background="#353446",
                    foreground="#CAA9E0",
                    fontsize=15,
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
                    format="%d-%m-%Y %H:%M:%S",
                    background="#282738",
                    foreground="#CAA9E0",
                    font="JetBrains Mono Bold",
                    fontsize=15,
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
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


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


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
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
        Match(wm_class="Arandr"),
        Match(wm_class="feh"),
        Match(wm_class="Galculator"),
        Match(title="branchdialog"),
        Match(title="Open File"),
        Match(title="pinentry"),
        Match(wm_class="ssh-askpass"),
        Match(wm_class="lxpolkit"),
        Match(wm_class="Lxpolkit"),
        Match(wm_class="yad"),
        Match(wm_class="Yad"),
        Match(wm_class="Cairo-dock"),
        Match(wm_class="cairo-dock"),
        Match(wm_class="megasync"),
        Match(wm_class="Xdm-app"),
    ],
    fullscreen_border_width=0,
    border_width=0,
)
auto_fullscreen = True

focus_on_window_activation = "smart"  # or smart or focus

wmname = "LG3D"
