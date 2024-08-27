# Todo: An infinty stopwatch timer with asynchronous function using Flutter Flet Framework 

from flet import *
import time
import asyncio

class Counter_Class(UserControl):
    def __init__(self, page: Page, col:Column):
        self.page = page
        self.col = col
        self.paused = False  # Variable to check if the timer is paused
        self.elapsed_time =0 # Store elapsed time when paused
        self.running = False #veriable to check if the timer  is running

        self.start = IconButton(
            icon=icons.PLAY_CIRCLE_FILLED_OUTLINED,
            icon_color="blue400",
            icon_size=20,
            tooltip="Start record",
            on_click=self.start_timer  # Attach start_timer function to on_click event
        
        )

        self.stop = IconButton(
            icon=icons.DELETE_FOREVER_ROUNDED,
            icon_color="pink600",
            icon_size=20,
            tooltip="Delete record",
            on_click=self.stop_timer # Attach stop_timer function to on_click event
        )
        
        self.text = Text("00:00:00", color=colors.BLACK,)
        self.stoper = None  # Placeholder to store the reference to the Container

    def build_timer(self):
        self.stoper = Container(
            width=300,
            height=50,
            bgcolor="#a8c7fa",
            border_radius=30,
            content=Row(
                controls=[self.text, self.start, self.stop],
                spacing=10,  # Add spacing between containers
                alignment=MainAxisAlignment.CENTER,
            )
        )
        return self.stoper
    
    async def update_timer(self):
        start_time = time.time() - self.elapsed_time # Adjust start time based on elapsed time
        while self.running:
            self.elapsed_time = time.time()-start_time # calculate the elaspsed time
            minutes, seconds = divmod(self.elapsed_time ,60)
            hours, minutes = divmod(minutes, 60)    
            self.text.value = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            self.page.update()
            await asyncio.sleep(1) # wait for 1 second before updating the time
    
    def start_timer(self, e):
        self.start.icon = icons.PAUSE_CIRCLE_FILLED_OUTLINED    
        self.start.tooltip= f"Pause record",
        if not self.running:
            self.running = True
            self.paused = False
            asyncio.run(self.update_timer())  # Run the async timer function
            self.page.update()
        elif self.running and not self.paused:
            self.paused = True  # Pause the timer
            self.running = False  # Pause the timer
            self.start.icon = icons.PLAY_CIRCLE_FILLED_OUTLINED
            self.start.tooltip=f"Play record",
            
        self.page.update()

    def stop_timer(self, e):
        self.running = False
        if self.stoper in self.col.controls:  # Ensure the container is in the controls list
            self.col.controls.remove(self.stoper)  # Remove the timer's container from the column
            self.page.open(SnackBar(Text("Stoper was deleted successfully!")))
            self.page.update()


def main(page:Page):
    page.title  = "Stopwatch" # Set the title of the page
    page.bgcolor = "#2c303d" # Set the background color of the page

    page.appbar = AppBar(
        leading=Icon(icons.STOP_CIRCLE_OUTLINED),
        leading_width=40,
        title=Text("StopWatch"),
        center_title=True,
        bgcolor=colors.BLUE_700,
    )

    col = Column(
        spacing=10,
        height=600,
        scroll=ScrollMode.ALWAYS,
        on_scroll_interval=0,
    )
    
    page.add(col)

    def add_counter(e):
        counter = Counter_Class(page, col)
        col.controls.append(counter.build_timer())
        page.open(SnackBar(Text("Stoper was added successfully!")))
        page.update()

    button = FloatingActionButton( "Add Timer",  icon=icons.ADD,
                                foreground_color="black",
                                on_click=add_counter,
                                bgcolor="#a8c7fa")
    page.add(button)
    page.update()

app(target=main)