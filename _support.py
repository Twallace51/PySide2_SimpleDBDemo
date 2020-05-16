"""Project Support:

Goals- provide for various projects:
    development/debugging tools
    commonly used generic methods and files,  eg
        data validation
        debugging
        confirm/notifications
        event filtering
        memory space for project global variables

The following methods and classes are all written for generic use by different projects.
Therefore,  avoid project specific edits below ....

Note about global variables:
    Global variables are useful in a project,  for example:
        to navigate between windows
        to pass the id of last database record accesed,  to different methods and windows
    Like all Python variables,   global variables are dynamic
    and can be created anywhere/anytime in a project.
    In this demo,  any module that imports this module using
        import _support as glb
    can access any variable declared with the format
        glb.<variable_name>
"""
if __name__ == '__main__':
    """this ensures project starts properly from any module"""
    import _RUN_ME    # pylint: disable = unused-import

if "imports needed below":
    """Note: p ylint below is not mispelled,  just temporarily and easily disabled"""
    #p ylint: disable = unused-import, ungrouped-imports

    import sys
    import re
    import datetime
    import inspect
    import os

    import PySide2.QtWidgets as W
    import PySide2.QtCore as C
    import PySide2.QtSql as S

if "development utilities":

    def debug(msg=None):
        """ returns module and line number wherever has been placed and called,
            with optional msg,  eg the current variable value,  etc
            Its use is intermediate between using a simple print() and breakpoint() during debugging
        """
        callerframerecord = inspect.stack()[1] # 0 represents this lineno, 1 for lineno in caller module
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        if msg:
            yellow("debug() message:  {}  #{}   {}()    {}".format(os.path.basename(info.filename), info.lineno, info.function, msg))
        else:
            yellow("debug() message:  {}  #{}   {}()".format(os.path.basename(info.filename), info.lineno, info.function))

if "database utilities":

    def open_database(database_name):
        """ """
        conn = S.QSqlDatabase.addDatabase('QSQLITE')
        conn.setDatabaseName(database_name)
        if not conn.open():
            msg1 = """Cannot open database, Unable to establish a database connection.
             Click Cancel to exit.     """
            alert(conn.databaseName() + msg1)
            sys.exit(1)

    def debug_sql(query, sql_str=None):
        """sql diagnostics - should be placed after following statements
            query = QSqlQuery()
            query.exec_(str_sql):
            query.first()
            sql_msg(query)
        """
        if query.isActive():
            if query.isSelect():
                if not query.first():
                    print('SELECT query successful,  but query is empty == no records')
                else:
                    green('SELECT query succeded:')
            else:
                green('UPDATE query succeded:')
                print("query.executedQuery()  == ", end='')
            green(query.executedQuery())
        else:
            red(sql_str)
            alert('query failed:')

if "QMessages":
    """Using these snippets of QMesageBox code helps make the mainline code easier to read and understand... """
    def notify_(title="Notification:", message=None):
        """Notification,  with corresponding message"""
        msg_box = W.QMessageBox()
        msg_box.setWindowTitle(title)
        if message:
            msg_box.setText(message.ljust(60))
        else:
            msg_box.setText(" ".ljust(80))

        msg_box.addButton(W.QMessageBox.Ok)
        msg_box.setIcon(W.QMessageBox.Information)
        msg_box.exec_()

    def confirm_(title="Confirmation:", options="Click [Ok] to proceed or [Cancel]"):
        """Asks to confirm or cancel an operation - returns True or False"""
        msg_box = W.QMessageBox()
        msg_box.setWindowTitle(title)
        if options:
            msg_box.setText(options.ljust(60))
        msg_box.addButton(W.QMessageBox.Ok)
        msg_box.addButton(W.QMessageBox.Cancel)
        msg_box.setIcon(W.QMessageBox.Question)
        if msg_box.exec_() == W.QMessageBox.StandardButton.Ok:
            return True
        return False

    def pending():
        """
        Code for this option still under development ...
        """
        W.QMessageBox.about(None, "Pending", pending.__doc__)

    def warning(msg=None, parent=None):
        """Warning message .... \n"""
        red(warning.__doc__ + msg)
        #msg="<font size = 6 color = red >" + warning.__doc__ + msg + "</font>"  # deprecated HTML format
        msg = '<h3 style="color: red;">'+ warning.__doc__ + msg + '</h3>'           # HTML using CSS format
        msg_box = W.QMessageBox()
        msg_box.about(parent, "Warning", msg)

    def unauthorized_msg(user_name="Guest"):
        """typically used to notify a user that tries to select an restricted operation,
        for example,   administrative functions"""
        msg_box = W.QMessageBox()
        msg_box.setWindowTitle("Unauthorized:")
        msg = "As {},  you do not have authorization for this option".format(user_name)
        msg = '<h3 style="color: red;">'+ msg + '</h3>' # HTML using CSS format
        msg_box.setText(msg.ljust(60))
        msg_box.addButton(W.QMessageBox.Ok)
        msg_box.setIcon(W.QMessageBox.Warning)
        msg_box.exec_()

if "generic methods":

    def is_valid_date(date_str):
        """checks if date string has following format  'YYYY-MM-DD'
        returns True/False"""
        #Note:  QLineEdit object also has additional validation and input mask functions included ....
        if re.fullmatch("20[0-2][0-9]-[0-1][0-9]-[0-3][0-9]", date_str) is None:
            print('date {} is in invalid format'.format(date_str))
            return False
        """is 'YYYY-MM-DD' a valid date? """
        #pylint: disable = invalid-name
        Y = int(date_str[0:4])
        M = int(date_str[5:7])
        D = int(date_str[8:10])
        try:
            datetime.date(Y, M, D)
        except ValueError:
            red('date {} is an invalid date'.format(date_str))
            warning('date {} is an invalid date'.format(date_str))
            return False
        return True

    def get_window_placement(application):
        """"returns default window placement for windows when a project is run on different monitors"""
        screen = application.primaryScreen().size()    # screen.geometry() -->  QRect(y, x, w, h)
        scr_width = screen.width()
        scr_height = screen.height()
        win_width = int(screen.width()*0.45)
        top_margin = int(screen.height()/20)
        win_height = scr_height-top_margin-20
        left_margin = int(scr_width/2)
        #debug("{} {}  {} {}  {}   y, x, w, h, screen".format(left_margin, top_margin, win_width, win_height, screen))
        return (C.QRect(left_margin, top_margin, win_width, win_height), screen)

if "ansi color codes":
    """following are useful for color highlighting of terminal output """
    # pylint: disable = missing-docstring,  multiple-statements
    def clear_scr(): print("\u001b[2J")
    def red(msg): print("\u001b[38;5;196m"+ str(msg) + "\u001b[0m"); return True
    def green(msg): print("\u001b[38;5;82m" + str(msg) + "\u001b[0m"); return True
    def greenish(msg): print("\u001b[38;5;192m" + str(msg) + "\u001b[0m"); return True
    def yellow(msg): print("\u001b[38;5;226m" + str(msg) + "\u001b[0m"); return True
    def yellowish(msg): print("\u001b[38;5;229m" + str(msg) + "\u001b[0m"); return True
    def blue(msg): print("\u001b[38;5;27m" + str(msg) + "\u001b[0m"); return True
    def mag(msg): print("\u001b[38;5;129m" + str(msg) + "\u001b[0m"); return True
    def cyan(msg): print("\u001b[38;5;51m" + str(msg) + "\u001b[0m"); return True
    def white(msg): print("\u001b[38;5;255m" + str(msg) + "\u001b[0m"); return True

    def orange(msg): print("\u001b[38;5;202m" + str(msg) + "\u001b[0m"); return True
    def gold(msg): print("\u001b[38;5;208m" + str(msg) + "\u001b[0m"); return True
    def pink(msg): print("\u001b[38;5;168m" + str(msg) + "\u001b[0m"); return True
    def alert(msg): print("\u001b[38;5;196m\u001b[5m" + str(msg) + "\u001b[0m"); return True  # flashing warning

if "event filtering options":
    """ event filtering can be assigned for an entire project and/or for individual widgets in a project
        event filtering can:
            help to see what is going on during development
            substitute for widget signals
            handle complicated responses to user input
        Usage:
            subclass eventFilter(obj, event) in a module
                and write a custom event filter
                or assign one of following ....
    """
    #pylint: disable = bad-continuation

    if "test methods for type of event":
        """the following are support functions for the methods below ...."""

        def in_key_events(event):
            """comment QEvent to remove it from report to terminal """
            if event.type() in (
                C.QEvent.KeyPress, # Key press ( QtGui.QKeyEvent)
                C.QEvent.KeyRelease, # Key release ( QtGui.QKeyEvent)
                ):
                return True
            return False

        def in_widget_events(event):
            """comment QEvent to remove it from report to terminal """
            if event.type() in (
                C.QEvent.FocusIn, # Widget or Window gains keyboard focus ( QtGui.QFocusEvent)
                #C.QEvent.FocusOut, # Widget or Window loses keyboard focus ( QtGui.QFocusEvent)
                #C.QEvent.ChildAdded, # An object gets a child ( QtCore.QChildEvent)
                #C.QEvent.ChildPolished, # A widget child gets polished ( QtCore.QChildEvent)
                #C.QEvent.ChildRemoved, # An object loses a child ( QtCore.QChildEvent)
                C.QEvent.EnabledChange, # Widget’s enabled state has changed
                C.QEvent.StyleChange, # Widget’s style has been changed

                #C.QEvent.Polish, # The widget is polished
                #C.QEvent.PolishRequest, # The widget should be polished, event handler to do last-minute initializations of the widget, if needed
                #C.QEvent.MacSizeChange, # The user changed his widget sizes ( macOS only)
                C.QEvent.ShowToParent, # A child widget has been shown
                #C.QEvent.HideToParent, # A child widget has been hidden
                #C.QEvent.UpdateLater, # The widget should be queued to be repainted at a later time
                C.QEvent.Show, # Widget was shown on screen ( QtGui.QShowEvent)
                #C.QEvent.Hide, # Widget was hidden ( QtGui.QHideEvent)
                #C.QEvent.Close, # Widget was closed ( QtGui.QCloseEvent)
                #C.QEvent.Move, # Widget’s position changed ( QtGui.QMoveEvent)
                #C.QEvent.FocusAboutToChange, # Widget or Window focus is about to change (QtGui.QFocusEvent)
                C.QEvent.FontChange, # Widget’s font has changed
                #C.QEvent.Paint, # Screen update necessary ( QtGui.QPaintEvent)
                C.QEvent.Resize, # Widget’s size changed (QtGui.QResizeEvent)
                ):
                return True
            return False

        def in_mouse_events(event):
            """
            selected events related to using mouse
            events disabled:
                MouseMove               since so many move events are reported
                HoverMove               ditto
                MouseButtonRelease      allways follows ButtonPress ...
            """
            if event.type() in (
                C.QEvent.Enter, # Mouse enters widget’s boundaries              ( QtGui.QEnterEvent)
                C.QEvent.Leave, # Mouse leaves widget’s boundaries
                C.QEvent.HoverEnter, # The mouse cursor enters a hover widget       ( QtGui.QHoverEvent)
                C.QEvent.HoverLeave, # The mouse cursor leaves a hover widget       ( QtGui.QHoverEvent)
                #C.QEvent.HoverMove, # The mouse cursor moves inside a hover widget ( QtGui.QHoverEvent)
                C.QEvent.MouseButtonDblClick, # Mouse press again               ( QtGui.QMouseEvent)
                C.QEvent.MouseButtonPress, # Mouse press                        ( QtGui.QMouseEvent)
                #C.QEvent.MouseButtonRelease, # Mouse release                   ( QtGui.QMouseEvent)
                #C.QEvent.MouseMove, # Mouse move                               ( QtGui.QMouseEvent)
                C.QEvent.MouseTrackingChange, # The mouse tracking state has changed
                C.QEvent.Wheel, # Mouse wheel rolled                            (QtGui.QWheelEvent)
                #C.QEvent.CursorChange, # The widget’s cursor has changed
                C.QEvent.NonClientAreaMouseButtonDblClick, # A mouse double click occurred outside the client area  (QtGui.QMouseEvent)
                C.QEvent.NonClientAreaMouseButtonPress, # A mouse button press occurred outside the client area     (QtGui.QMouseEvent)
                C.QEvent.NonClientAreaMouseButtonRelease, # A mouse button release occurred outside the client area (QtGui.QMouseEvent)
                C.QEvent.NonClientAreaMouseMove, # A mouse move occurred outside the client area                    (QtGui.QMouseEvent)
                C.QEvent.UngrabMouse, # Item loses mouse grab                   (QtWidgets.QGraphicsItem , QtQuick.QQuickItem)
                C.QEvent.WhatsThisClicked, # A link in a widget’s “What’s This?” help was clicked
                ):
                return True
            return False

        def in_remaining_events(event):
            """comment QEvent lines below,  to remove event from reporting to the terminal """
            if event.type() in (
                #C.QEvent.Timer, # Regular timer events             (QtCore.QTimerEvent)
                #C.QEvent.UpdateRequest, # The widget should be repainted
                C.QEvent.Clipboard, # The clipboard contents have changed

                # drag events
                C.QEvent.DragEnter, # The cursor enters a widget during a drag and drop operation (QtGui.QDragEnterEvent)
                C.QEvent.DragLeave, # The cursor leaves a widget during a drag and drop operation (QtGui.QDragLeaveEvent)
                C.QEvent.DragMove, # A drag and drop operation is in progress (QtGui.QDragMoveEvent)
                C.QEvent.Drop, # A drag and drop operation is completed (QtGui.QDropEvent)

                # GraphicsScene
                C.QEvent.GraphicsSceneContextMenu, # Context popup menu over a graphics scene (QtWidgets.QGraphicsSceneContextMenuEvent)
                C.QEvent.GraphicsSceneDragEnter, # The cursor enters a graphics scene during a drag and drop operation (QtWidgets.QGraphicsSceneDragDropEvent)
                C.QEvent.GraphicsSceneDragLeave, # The cursor leaves a graphics scene during a drag and drop operation (QtWidgets.QGraphicsSceneDragDropEvent)
                C.QEvent.GraphicsSceneDragMove, # A drag and drop operation is in progress over a scene (QtWidgets.QGraphicsSceneDragDropEvent)
                C.QEvent.GraphicsSceneDrop, # A drag and drop operation is completed over a scene (QtWidgets.QGraphicsSceneDragDropEvent)
                C.QEvent.GraphicsSceneHelp, # The user requests help for a graphics scene (QtGui.QHelpEvent)
                C.QEvent.GraphicsSceneHoverEnter, # The mouse cursor enters a hover item in a graphics scene (QtWidgets.QGraphicsSceneHoverEvent)
                C.QEvent.GraphicsSceneHoverLeave, # The mouse cursor leaves a hover item in a graphics scene (QtWidgets.QGraphicsSceneHoverEvent)
                C.QEvent.GraphicsSceneHoverMove, # The mouse cursor moves inside a hover item in a graphics scene (QtWidgets.QGraphicsSceneHoverEvent)
                C.QEvent.GraphicsSceneMouseDoubleClick, # Mouse press again (double click) in a graphics scene (QtWidgets.QGraphicsSceneMouseEvent)
                C.QEvent.GraphicsSceneMouseMove, # Move mouse in a graphics scene (QtWidgets.QGraphicsSceneMouseEvent)
                C.QEvent.GraphicsSceneMousePress, # Mouse press in a graphics scene (QtWidgets.QGraphicsSceneMouseEvent)
                C.QEvent.GraphicsSceneMouseRelease, # Mouse release in a graphics scene (QtWidgets.QGraphicsSceneMouseEvent)
                C.QEvent.GraphicsSceneWheel, # Mouse wheel rolled in a graphics scene (QtWidgets.QGraphicsSceneWheelEvent)
                C.QEvent.GraphicsSceneMove, # Widget was moved ( QtWidgets.QGraphicsSceneMoveEvent)
                C.QEvent.GraphicsSceneResize, # Widget was resized          ( QtWidgets.QGraphicsSceneResizeEvent)

                # Layouts
                C.QEvent.InputMethodQuery, # A input method query event     (QtGui.QInputMethodQueryEvent)
                C.QEvent.KeyboardLayoutChange, # The keyboard layout has changed
                C.QEvent.LanguageChange, # The application translation changed
                C.QEvent.LayoutDirectionChange, # The direction of layouts changed
                C.QEvent.LayoutRequest, # Widget layout needs to be redone

                #
                C.QEvent.WindowActivate, # Window was activated
                #C.QEvent.WindowDeactivate, # Window was deactivated
                #C.QEvent.ActivationChange, # A widget’s top-level window activation state has changed
                #C.QEvent.ApplicationActivate, # This enum has been deprecated. Use instead
                C.QEvent.ApplicationActivated, # This enum has been deprecated. Use instead
                C.QEvent.ApplicationDeactivate, # This enum has been deprecated. Use instead
                C.QEvent.ApplicationFontChange, # The default application font has changed
                C.QEvent.ApplicationPaletteChange, # The default application palette has changed
                C.QEvent.ApplicationStateChange, # The state of the application has changed
                C.QEvent.ApplicationLayoutDirectionChange, # The default application layout direction has changed
                C.QEvent.ApplicationWindowIconChange, # The application’s icon has changed

                C.QEvent.ActionAdded, # A new action has been added ( QtGui.QActionEvent)
                C.QEvent.ActionChanged, # An action has been changed ( QtGui.QActionEvent)
                #C.QEvent.ActionRemoved, # An action has been removed ( QtGui.QActionEvent)

                C.QEvent.CloseSoftwareInputPanel, # A widget wants to close the software input panel (SIP)
                C.QEvent.ContentsRectChange, # The margins of the widget’s content rect changed
                C.QEvent.DeferredDelete, # The object will be deleted after it has cleaned up (QDeferredDeleteEvent)

                #C.QEvent.DynamicPropertyChange, # A dynamic property was added, changed, or removed from the object
                C.QEvent.EnterWhatsThisMode, # Send to toplevel widgets when the application enters “What’s This?” mode
                #C.QEvent.Expose, # Sent to a window when its on-screen contents are invalidated and need to be flushed from the backing store
                C.QEvent.FileOpen, # File open request (QtGui.QFileOpenEvent)
                C.QEvent.Gesture, # A gesture was triggered                     (QtWidgets.QGestureEvent)
                C.QEvent.GestureOverride, # A gesture override was triggered    (QtWidgets.QGestureEvent)
                C.QEvent.GrabKeyboard, # Item gains keyboard grab               (QtWidgets.QGraphicsItem only)
                C.QEvent.GrabMouse, # Item gains mouse grab                     (QtWidgets.QGraphicsItem only)

                C.QEvent.IconDrag, # The main icon of a window has been dragged away    (QtGui.QIconDragEvent)
                C.QEvent.IconTextChange, # Widget’s icon text has been changed.         (Deprecated)')
                C.QEvent.InputMethod, # An input method is being used                   (QtGui.QInputMethodEvent)

                C.QEvent.LeaveWhatsThisMode, # Send to toplevel widgets when the application leaves “What’s This?” mode
                C.QEvent.LocaleChange, # The system locale has changed

                C.QEvent.RequestSoftwareInputPanel, # A widget wants to open a software input panel (SIP)
                C.QEvent.MetaCall, # An asynchronous method invocation via QMetaObject.invokeMethod()
                C.QEvent.ModifiedChange, # Widgets modification state has been changed
                C.QEvent.OrientationChange, # The screens orientation has changes (QScreenOrientationChangeEvent)
                C.QEvent.PaletteChange, # Palette of the widget changed
                C.QEvent.ParentAboutToChange, # The widget parent is about to change
                C.QEvent.ParentChange, # The widget parent has changed
                C.QEvent.PlatformPanel, # A platform specific panel has been requested
                #C.QEvent.PlatformSurface, # A native platform surface has been created or is about to be destroyed (QPlatformSurfaceEvent)
                C.QEvent.QueryWhatsThis, # The widget should accept the event if it has “What’s This?” help (QtGui.QHelpEvent)
                C.QEvent.ReadOnlyChange, # Widget’s read-only state has changed (since Qt 5.4)
                C.QEvent.ScrollPrepare, # The object needs to fill in its geometry information (QtGui.QScrollPrepareEvent)
                C.QEvent.Scroll, # The object needs to scroll to the supplied position (QtGui.QScrollEvent)
                C.QEvent.Shortcut, # Key press in child for shortcut key handling (QtGui.QShortcutEvent)
                C.QEvent.ShortcutOverride, # Key press in child, for overriding shortcut key handling (QtGui.QKeyEvent)
                C.QEvent.SockAct, # Socket activated, used to implement QtCore.QSocketNotifier
                C.QEvent.StateMachineSignal, # A signal delivered to a state machine (QStateMachine.SignalEvent)
                C.QEvent.StateMachineWrapped, # The event is a wrapper for, i.e., contains, another event (QStateMachine.WrappedEvent)
                C.QEvent.StatusTip, # A status tip is requested (QtGui.QStatusTipEvent)

                C.QEvent.TabletMove, # Wacom tablet move (QtGui.QTabletEvent)
                C.QEvent.TabletPress, # Wacom tablet press (QtGui.QTabletEvent)
                C.QEvent.TabletRelease, # Wacom tablet release (QtGui.QTabletEvent)
                C.QEvent.TabletEnterProximity, # Wacom tablet enter proximity event (QtGui.QTabletEvent), sent to QtWidgets.QApplication
                C.QEvent.TabletLeaveProximity, # Wacom tablet leave proximity event (QtGui.QTabletEvent), sent to QtWidgets.QApplication
                C.QEvent.TabletTrackingChange, # The Wacom tablet tracking state has changed (since Qt 5.9)

                C.QEvent.ThreadChange, # The object is moved to another thread. This is the last event sent to this object in the previous thread. See QObject.moveToThread()

                C.QEvent.ToolBarChange, # The toolbar button is toggled on macOS
                C.QEvent.ToolTip, # A tooltip was requested                                        (QtGui.QHelpEvent)
                C.QEvent.WhatsThis, # The widget should reveal “What’s This?” help                  (QtGui.QHelpEvent)

                C.QEvent.ToolTipChange, # The widget’s tooltip has changed

                C.QEvent.TouchBegin, # Beginning of a sequence of touch-screen or track-pad events  (QtGui.QTouchEvent)
                C.QEvent.TouchCancel, # Cancellation of touch-event sequence                        (QtGui.QTouchEvent)
                C.QEvent.TouchEnd, # End of touch-event sequence                                    (QtGui.QTouchEvent)
                C.QEvent.TouchUpdate, # Touch-screen event                                          (QtGui.QTouchEvent)

                C.QEvent.UngrabKeyboard, # Item loses keyboard grab             (QtWidgets.QGraphicsItem only)
                C.QEvent.WinEventAct, # A Windows-specific activation event has occurred
                C.QEvent.WindowBlocked, # The window is blocked by a modal dialog
                C.QEvent.WindowIconChange, # The window’s icon has changed
                C.QEvent.WindowStateChange, # The window’s state (minimized, maximized or full-screen) has changed (QtGui.QWindowStateChangeEvent)
                C.QEvent.WindowTitleChange, # The window title has changed
                C.QEvent.WindowUnblocked, # The window is unblocked after a modal dialog exited
                #C.QEvent.WinIdChange, # The window system identifer for this native widget has changed
                C.QEvent.ScreenChangeInternal,
                ):
                return True
            return False

    if "show_events methods":
        """ the following can filter specifically for keyboard, widget, mouse events
            or (almost) all events"""

        def show_widget_events(obj, event):
            """ """
            if in_widget_events(event):
                string = str(event.type()).split('.')[4].split()[0] # get event name
                try:
                    obj = obj.text()
                except:
                    pass
                gold("{}\n   {}\n".format(string, obj))
            return False

        def show_mouse_events(obj, event):
            """ """
            if in_mouse_events(event):
                string = str(event.type()).split('.')[4].split()[0] # get event name
                try:
                    obj = obj.text()
                except:
                    pass

                if event.type() == C.QEvent.MouseButtonPress:
                    yellow(string)
                    yellow(obj)
                    gold('clicked at: ' + str(event.x()) + '  ' + str(event.y()) + '\n')
                else:
                    greenish("{}\n   {}\n".format(string, obj))
            return False

        def show_key_events(obj, event):
            """selected events related to key presses """
            if in_key_events(event):
                try: # for text string,   if available
                    text = obj.text()
                except:
                    text = ""
                string = str(event.type()).split('.')[4].split()[0] # get event name

                try:
                    string = string + '   ' + str(event.key()) + '  ' + chr(event.key())
                except ValueError:
                    string = string + '  not a character key    '

                yellow("{}\n   {}  {}\n".format(string, text, obj))

            return False

        def show_remaining_events(obj, event):
            """events not in mouse, key and widget groups """
            if in_remaining_events(event):
                try: # for text string,   if available
                    text = obj.text()
                except:
                    text = ""
                string = str(event.type()).split('.')[4].split()[0] # get event name

                yellowish("{}\n   {}  {}\n".format(string, text, obj))

            return False

        previous_type = None

        def show_most_events(obj, event):
            """
            report almost all events
            Note: repeated events are silenced here,   since some repeat very frequently,
            for example QEvent.MouseMove
            """
            global previous_type            #pylint: disable = global-statement
            if event.type() == previous_type:
                return False
            previous_type = event.type()

            show_widget_events(obj, event)
            show_mouse_events(obj, event)
            show_key_events(obj, event)
            show_remaining_events(obj, event)

            return False
