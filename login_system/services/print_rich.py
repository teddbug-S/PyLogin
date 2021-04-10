from os import get_terminal_size
from textwrap import fill
from random import choice

from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns

from resources.arts import profile_panel_user


class PrintRich:
    """
    A user of the rich module to handle rendering of data and
    terminal beautification.
    """

    def __init__(self) -> None:
        self.console = Console()
        self.panel = Panel
        self.column = Columns
        self.align = Align
        self.terminal_size = get_terminal_size()
        self.table = Table
        self.colors = [
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            'bright_black',
            'bright_red',
            'bright_green',
            'bright_yellow',
            'bright_blue',
            'bright_magenta',
            'bright_cyan',
            'bright_white',
            'grey0',
            'navy_blue',
            'dark_blue',
            'blue3',
            'blue1',
            'dark_green',
            'deep_sky_blue4',
            'dodger_blue3',
            'dodger_blue2',
            'green4',
            'spring_green4',
            'turquoise4',
            'deep_sky_blue3',
            'dodger_blue1',
            'green3',
            'spring_green3',
            'dark_cyan',
            'light_sea_green',
            'deep_sky_blue2',
            'deep_sky_blue1',
            'spring_green2',
            'cyan3',
            'dark_turquoise',
            'turquoise2',
            'green1',
            'spring_green1',
            'medium_spring_green',
            'cyan2',
            'cyan1',
            'dark_red',
            'deep_pink4',
            'purple4',
            'purple3',
            'blue_violet',
            'orange4',
            'grey37',
            'medium_purple4',
            'slate_blue3',
            'royal_blue1',
            'chartreuse4',
            'dark_sea_green4',
            'pale_turquoise4',
            'steel_blue',
            'steel_blue3',
            'cornflower_blue',
            'chartreuse3',
            'cadet_blue',
            'sky_blue3',
            'steel_blue1',
            'pale_green3',
            'sea_green3',
            'aquamarine3',
            'medium_turquoise',
            'chartreuse2',
            'sea_green2',
            'sea_green1',
            'aquamarine1',
            'dark_slate_gray2',
            'dark_magenta',
            'dark_violet',
            'purple',
            'light_pink4',
            'plum4',
            'medium_purple3',
            'slate_blue1',
            'yellow4',
            'wheat4',
            'grey53',
            'light_slate_grey',
            'medium_purple',
            'light_slate_blue',
            'dark_olive_green3',
            'dark_sea_green',
            'light_sky_blue3',
            'sky_blue2',
            'dark_sea_green3',
            'dark_slate_gray3',
            'sky_blue1',
            'chartreuse1',
            'light_green',
            'pale_green1',
            'dark_slate_gray1',
            'red3',
            'medium_violet_red',
            'magenta3',
            'dark_orange3',
            'indian_red',
            'hot_pink3',
            'medium_orchid3',
            'medium_orchid',
            'medium_purple2',
            'dark_goldenrod',
            'light_salmon3',
            'rosy_brown',
            'grey63',
            'medium_purple1',
            'gold3',
            'dark_khaki',
            'navajo_white3',
            'grey69',
            'light_steel_blue3',
            'light_steel_blue',
            'yellow3',
            'dark_sea_green2',
            'light_cyan3',
            'light_sky_blue1',
            'green_yellow',
            'dark_olive_green2',
            'dark_sea_green1',
            'pale_turquoise1',
            'deep_pink3',
            'magenta2',
            'hot_pink2',
            'orchid',
            'medium_orchid1',
            'orange3',
            'light_pink3',
            'pink3',
            'plum3',
            'violet',
            'light_goldenrod3',
            'tan',
            'misty_rose3',
            'thistle3',
            'plum2'
        ]

    def get_random_color(self):
        return choice(self.colors)

    def print_welcome_panel(self, text):
        """
        Displays a welcome panel to the console
        """
        title = "[red bold]Welcome[/red bold] [yellow bold]To[/yellow bold] [blue bold]PyLogin🐍[/blue bold]"
        welcome_text = text
        welcome_panel = self.panel(
            welcome_text,  # renderable
            title=title,  # title
            title_align='center',  # align
            border_style=' yellow',  # border style
            width=80
        )
        self.console.print(" " * 34 + "🌟🌟⭐🌟🌟", justify='left')
        self.console.print(welcome_panel)
        self.console.print('   ', '⚡' * self.terminal_size.lines)

    def print_data_table(self, data, title):
        """
        Prints the tabulated data to the console
        """
        table = self.table(
            show_header=True,
            title=title,
            style='yellow',
            border_style='green dim',
            show_edge=True,
            pad_edge=True,
            header_style='bold blue'
        )
        column_rendered = False
        for data in data:
            if column_rendered:  # if column already rendered
                pass  # do nothing
            else:  # render column
                for key in data:
                    if key in ('blockstatus', 'verified'):
                        table.add_column(f"{key.title()}", style='purple blink')
                    elif key == 'username':
                        table.add_column(f"{key.title()}", style='cyan')
                    elif key == 'age':
                        table.add_column(key.title(), style='violet')
                    elif key == 'password':
                        table.add_column(f"{key.title()}", style='red')
                    else:
                        table.add_column(key.title(), style='yellow')
            column_rendered = True

            table.add_row(*data.values())
        self.console.print(table, justify='center')

    def print_data_panel(self, data, panel_profile):
        """
        Renders data in rich panel
        """
        renderables = []
        for data in data:
            format_map = {
                'username': data.get('username'),
                'firstname': data.get('firstname'),
                'lastname': data.get('lastname'),
                'age': data.get('age'),
                'blockstatus': bool(data.get('blockstatus')),
                'verified': bool(data.get('verified')),
                'email': data.get('email'),
                'type': data.get('type')
            }
            profile = panel_profile.format_map(format_map)
            color = self.get_random_color()
            panel = self.panel(
                profile,
                title=f"[bold {color}]Information on {format_map['username']} [/bold {color}]",
                title_align='center',
                width=40,
                border_style=f'{self.get_random_color()} blink2'
            )
            renderables.append(panel)
        self.console.print("\n\n")
        self.console.print(self.column(renderables))

    def print_home_data(self, data, home_template):
        """
        Displays data in a panel for the home screen
        """
        renderables = []
        for data in data:
            username = data['username']  # get username
            color = self.get_random_color()  # random color for username
            full_template = [f"[{color} blink]{username}[/{color} blink]\n\n"]
            bio = fill(data['bio'], 26).strip().splitlines(False)  # get bio
            # get logo
            logo = home_template.splitlines(False)
            # check if logo is bigger than the bio and add empty string in order to avoid errors
            if (length := len(logo) - len(bio)) >= 1:
                for _ in range(length):  # loop in range of the interval
                    bio.append('')  # while looping append empty string
            for art, line in zip(logo, bio):
                if art:  # check if we still have the art
                    line = f"  {line}\n"
                else:
                    art = f"{len(bio[2]) * ' '}  "
                # random color for the text in a line
                color = self.get_random_color()
                text = "[{color}]{text}[/{color}]".format(color=color, text=art + line.rstrip('\n'))
                full_template.append(text)  # append text to list
            # create the panel
            # print('\n'.join(full_template))
            panel = self.panel(
                '\n'.join(full_template),  # join text with line breaks
                width=50,  # width of panel
                border_style=f'{self.get_random_color()} blink'
            )
            renderables.append(panel)
        self.console.print("\n\n")
        self.console.print(self.column(renderables))

    def my_profile_display(self, *, data, progress, panel_template) -> None:
        """
        Serves the my profile screen in user mode.

        :param panel_template: template to use for information, might be user or admin template
        :param progress: the progress made in the profile strength
        :param data: user's data
        """
        bio = f"{fill(data.get('bio'), 38)}" if bool(data.get('bio')) else "[sky_blue2 blink] Please update bio [" \
                                                                           "/sky_blue2 blink] "
        data['verified'] = bool(data.get('verified'))
        data['blockstatus'] = bool(data.get("blockstatus"))
        ascii_arts = {
            50: """
          .---------------------------.
          | [____PROFILE  STATUS____] |
          |  ________________________ |
          | |:::::::::50%|           ||
          | `"""""""""""""""""""""""" |
          '---------------------------'
        """,
            80: """,
          .---------------------------.
          | [____PROFILE  STATUS____] |
          |  ________________________ |
          | |:::::::::::::::80%|     ||
          | `"""""""""""""""""""""""" |
          '---------------------------'
        """,
            100: """
          .---------------------------.
          | [____PROFILE  STATUS____] |
          |  ________________________ |
          | |::::::::::::::::::::100%||
          | `"""""""""""""""""""""""" |
          '---------------------------'
        """,
            "batman_logo": """
    [yellow blink]
              _,    _   _    ,_
         .o888P     Y8o8Y     Y888o.
        d88888      88888      88888b
       d888888b_  _d88888b_  _d888888b
       8888888888888888888888888888888
       8888888888888888888888888888888
       Y8888P"Y888P"Y888P"Y888P"Y8888P
        Y888   '8'   Y8P   '8'   888Y
         '8o          V          o8'
           `                     `[/yellow blink]
                """,
        }

        color = self.get_random_color()
        progress_art = f"""
        [{color}]{ascii_arts.get(progress)} 
[/{color}]
        """
        action_art = f"""
         {ascii_arts.get("batman_logo")}
         [green]Your account is verified.✅🌟[/green]
        """

        panels = [
            Panel(
                title=f"[bright_yellow]Information on {data.get('username')}[/bright_yellow]",
                title_align="left",
                renderable=panel_template.format_map(data),
                border_style='red blink',
            ),
            Panel(
                title='[purple]Bio[/purple]',
                title_align='right',
                renderable=bio if bio else "[pink3 blink align center] Please update bio [/pink3 blink align center]",
                border_style='green bold',
            ),
            Panel(
                title='[magenta]Action[/magenta]',
                title_align='center',
                renderable=action_art,
                width=50,
                border_style='gold3'

            ),
            Panel(
                title='[cyan]Profile Strength[/cyan]',
                title_align='right',
                renderable=progress_art,
                width=50,
                border_style='gold3'

            )
        ]

        renderables = Columns(panels, equal=True)
        panel = Panel(
            renderables,
            title='[bright_yellow]User Profile[/bright_yellow]',
            title_align='left',
            width=109,
            # expand=True,
            border_style="pink3"
            # padding=(14, 4)
        )
        self.console.print(panel, justify='center')
