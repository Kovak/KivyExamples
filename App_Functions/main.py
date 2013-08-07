from kivy.app import App
from kivy.uix.widget import Widget


class RootWidget(Widget):
    pass

class AppFunctionsApp(App):
    def build(self):
        '''
        Initialized the application, if you return a widget that widget will 
        be used as the root widget. In the kv method of declaring the root 
        widget, we do not return a widget here.
        '''
        pass

    def on_pause(self):
        '''
        Called when App pauses, Must return true to be able to pause app
        Default is false
        '''
        return True

    def on_resume(self):
        #Called when app ends pause mode
        pass

    def on_start(self):
        #Ran once on startup after intialization
        pass

    def on_stop(self):
        #Ran once when app finishes running
        pass

if __name__ == '__main__':
    '''
    By default the app looks for a kvfile named after the app class - App at 
    the end The default kv name for this file is 'appfunctions.kv', you can 
    change the file loaded by passing this arg
    '''
    AppFunctionsApp(kv_file = 'nondefaultkvname.kv').run()
