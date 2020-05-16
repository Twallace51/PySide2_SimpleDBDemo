#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""python project template demo ...

    sets a default window size,  based on current screen size
    opens database test.db,  with table table_1
    opens List, Form, Search and Login windows
    adds following to menu in menu window
        --> list_window for 'table_1'
        --> login for admin name and password
    opens main menu window for user input

For more details,  see  _README.gny

To run this application,  run  (this file) _RUN_ME.py

Adapted by:   twallace51@gmail.com
    Cochabamba,  Bolivia
    using Linux Lubuntu, Python 3.8.2, PySide2 5.14.4,  geany 1.35   pylint3

"""
#p ylint: disable = fixme

"""Note about how python runs this files´s code:
Python runs following code from top to bottom,  where:
    imports are recursively and sequentially inserted into runtime code
        and also then run (duplicate imports skipped?)
    when found above, the following are loaded and immediately available (using corresponding import prefix)
        variable assignments
        methods
        classes
    Also when classes are found:
        the parent class is also imported and run
        all __init__ methods of classes and their parents,
        are sequentially appended to end of runtime code and finally also run
    If a class instance has been created,
        the following are loaded and immediately available (using corresponding instance prefix)
            instance variable assignments
            class methods
    """

#pylint: disable = ungrouped-imports, import-error, unused-import

if 'imports':
    import sys
    import _support as glb              # all variables, methods and classes available with glb.* prefix
    from _support import(
        debug,
        open_database,
        notify_,
        confirm_,
        get_window_placement,
        unauthorized_msg,
        )

    if "PySide2":
        #pylint: disable = unused-import
        import PySide2.QtGui as G
        import PySide2.QtWidgets as W
        import PySide2.QtCore as C

    if "Project":
        from Table_1 import(
            Table_1_List,
            Table_1_Form,
            Table_1_Search,
            )

class Login(W.QDialog):
    """
    Assumes parameters  (user_list, parent_window=None)
    If user_name and password are in user_list,  glb.current_user set to user_name
    Then,  test in code for current_user and if user is authorized or not,  to continue ..."""

    def __init__(self, user_list):
        W.QDialog.__init__(self)
        self.resize(450, 150)
        self.setWindowTitle("   Enter username and password   ")
        self.user_list = user_list

        if "widgets":
            self.text_name = W.QLabel("Username:", self)

            self.text_pass = W.QLabel("Password:", self)

            self.input_name = W.QLineEdit(self)
            self.input_name.setClearButtonEnabled(True)

            self.input_pass = W.QLineEdit(self)
            self.input_pass.setEchoMode(W.QLineEdit.Password)
            self.input_pass.setClearButtonEnabled(True)

            self.login_btn = W.QPushButton(self)
            self.login_btn.setText('Click to Login')

            ##self.login_btn.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
            self.login_btn.setStyleSheet('QPushButton {background-color: darkGray; color: darkBlue;}')

        self.login_btn.clicked.connect(self.login_handler)

        if "layout":
            layout = W.QVBoxLayout(self)
            layout.addWidget(self.text_name)
            layout.addWidget(self.input_name)
            layout.addWidget(self.text_pass)
            layout.addWidget(self.input_pass)
            layout.addWidget(self.login_btn)

    def login_handler(self):
        """ """
        if "message box":
            msg_box = W.QMessageBox()
            msg_box.setIcon(W.QMessageBox.Information)
            msg_box.setStandardButtons(W.QMessageBox.Ok)
            green = '<font color="#009900">'
            red = '<font color="#ff0000">'

        if (self.input_name.text(), self.input_pass.text()) in self.user_list:
            glb.current_user = self.input_name.text()
            msg_box.setWindowTitle("VALID")
            msg_box.setText(green + "user name and password ACCEPTED".ljust(60))
            msg_box.setInformativeText("Logged in as {}".format(self.input_name.text()))
            self.accept()
        else:
            glb.current_user = "Guest"
            msg_box.setWindowTitle("ERROR")
            msg_box.setText(red + "Bad user and/or password - INVALID ".ljust(60))
            msg_box.setInformativeText("Logged in as Guest")
            self.reject()

        self.hide()
        self.input_name.clear()
        self.input_pass.clear()
        msg_box.exec_()

if "login functions":

    def login_act_handler():
        """ """
        print("""
During development, try following:
    user name:     Admin
    user password  admin
In a run time project, remember to:
    delete this message
    update login variables in _RUN_ME.py
        glb.admin_user_list
        glb.user_list
        """)
        glb.login.exec_()

    def admin_option_handler():
        """ """
        if glb.current_user not in glb.admin_user_list:
            unauthorized_msg(glb.current_user)
            return
        glb.pending()

class MenuWindow(W.QWidget):
    """ MenuWindow class provides a basic menu bar, allowing:
            admin login
            about app messages
    """
    def __init__(self):
        W.QWidget.__init__(self)

        if "attributes":
            self.setWindowTitle("Main Window")
            self.setMinimumSize(160, 160)
            self.setGeometry(glb.win_placement)

        if "menu bar options":

            if "create menubar actions":
                self.login_act = W.QAction("Enter Admin password to enable admin menus", self)
                self.about_qt_act = W.QAction("Show the Qt library's About box", self)
                self.about_app_act = W.QAction("Show the application's About box", self)

                self.open_table_1_list_act = W.QAction("Open Table_1 List", self)
                self.option_1_act = W.QAction("Option message 1", self)
                self.option_2_act = W.QAction("Option message 2", self)
                self.option_3_act = W.QAction("Option message 3", self)

                self.admin_1_act = W.QAction("Admin option 1", self)
                self.admin_2_act = W.QAction("Admin option 2", self)
                self.admin_3_act = W.QAction("Admin option 3", self)

            if "set shortcut":
                self.about_app_act.setShortcut("Ctrl+A")

                self.option_1_act.setShortcut("Ctrl+1")
                self.option_2_act.setShortcut("Ctrl+2")
                self.option_3_act.setShortcut("Ctrl+3")

            if "set action icons":
                self.login_act.setIcon(G.QIcon(glb.icons + '/apps/preferences-desktop-user-password.png'))
                self.about_qt_act.setIcon(G.QIcon(glb.icons + '/actions/help-about.png'))
                self.about_app_act.setIcon(G.QIcon(glb.icons + '/actions/help-about.png'))

                self.admin_1_act.setIcon(G.QIcon(glb.icons + '/categories/system-help.png'))
                self.admin_2_act.setIcon(G.QIcon(glb.icons + '/categories/system-help.png'))
                self.admin_3_act.setIcon(G.QIcon(glb.icons + '/categories/system-help.png'))

                self.open_table_1_list_act.setIcon(G.QIcon(glb.icons + '/actions/view-financial-list.png'))
                self.option_1_act.setIcon(G.QIcon(glb.icons + '/categories/system-help.png'))
                self.option_2_act.setIcon(G.QIcon(glb.icons + '/categories/system-help.png'))
                self.option_3_act.setIcon(G.QIcon(glb.icons + '/categories/system-help.png'))

            if "set triggered connections":
                self.login_act.triggered.connect(login_act_handler)
                self.about_qt_act.triggered.connect(W.QApplication.instance().aboutQt)    #self.about_qt_act.triggered.connect(qApp.aboutQt) # also works
                self.about_app_act.triggered.connect(
                    lambda: W.QMessageBox.about(self, "About Cuentas", __doc__))

                self.open_table_1_list_act.triggered.connect(self.open_table_1_list_handler)
                self.option_1_act.triggered.connect(glb.pending)
                self.option_2_act.triggered.connect(glb.pending)
                self.option_3_act.triggered.connect(glb.pending)

                self.admin_1_act.triggered.connect(admin_option_handler)
                self.admin_2_act.triggered.connect(admin_option_handler)
                self.admin_3_act.triggered.connect(admin_option_handler)

            if "set initial menubar status":
                self.option_1_act.setEnabled(True)
                self.option_2_act.setEnabled(True)
                self.option_3_act.setEnabled(True)
                self.open_table_1_list_act.setEnabled(True)

        if "menu bar layout":

            self.menu_mbr = W.QMenuBar()

            if "Menu":
                self.main_mnu = self.menu_mbr.addMenu("&Menu")

                self.main_mnu.addAction(self.open_table_1_list_act)
                self.main_mnu.addAction(self.option_1_act)
                self.main_mnu.addAction(self.option_2_act)
                self.main_mnu.addAction(self.option_3_act)

            if "Admin":
                """
                Any menu option placed in this menu should be disabled by default, except for login_act
                Succesful login will enable any menu option found in admin_mnu,  see login_handler() below
                """
                self.admin_mnu = self.menu_mbr.addMenu("&Admin")
                self.admin_mnu.addAction(self.login_act)

                self.admin_mnu.addAction(self.admin_1_act)
                self.admin_mnu.addAction(self.admin_2_act)
                self.admin_mnu.addAction(self.admin_3_act)

            if "About":
                self.about_mnu = self.menu_mbr.addMenu("About")
                self.about_mnu.addAction(self.about_qt_act)
                self.about_mnu.addAction(self.about_app_act)

        if "main_layout":
            self.main_layout = W.QGridLayout(self)
            self.setLayout(self.main_layout)

            self.main_layout.setMenuBar(self.menu_mbr)

    if "connection handlers":

        def open_table_1_list_handler(self):
            """ """
            glb.table_1_list.filter_str = ''
            glb.table_1_list.update_table_1_list()
            glb.table_1_list.show()
            self.hide()

    if "sub classed methods":

        def closeEvent(self, event): #pylint: disable = invalid-name, unused-argument
            """
            QWidget function closeEvent() run when window [X] clicked,
            is subclassed here to prevent default closing of window and app - see below
            """
            self.close() # see below

        def eventFilter(self, obj, event):  #pylint: disable = no-self-use
            """use a generic eventFilter() like glb.show_most_events(obj, event) from _support.py,
            or write a custom global one here for project"""
            glb.show_most_events(obj, event)
            return False

if "project main script":
    glb.green(__doc__)

    app = W.QApplication()

    if "project global variables":
        """project global variables use the prefix glb.<variable>
        As in any python variable,  they are dynamic
            and can be initialized/updated at anytime/anywhere in a project.
        """
        glb.icons = "/usr/share/icons/oxygen/base/32x32"  # my prefered icon set

        if "set default window placement parameters":
            glb.screen_size = C.QSize(1920, 1050)                    # default screen_size
            glb.win_placement = C.QRect(800, 80, 500, 800)        # default window placement and size

        if "database variables":
            glb.db_name = "test.db"   # assumes is a sqlite database

        if "place holder for current record":
            glb.list_id = 1             # place holder for current table_1 record

        if "login parameters":   # TODO  - update following for run-time version!
            glb.user_list = [
                ("Admin", "admin"),
                ("Tim", "tim")]
            glb.admin_user_list = [
                ("Admin"),
                ("Tim")
                ]
            glb.current_user = "Guest"

    if not "customize window placement":
        glb.win_placement = get_window_placement(app)[0]
        glb.screen_size = get_window_placement(app)[1]

    open_database(glb.db_name)

    if "create project windows":
        glb.menu_win = MenuWindow()
        glb.table_1_list = Table_1_List()
        glb.table_1_form = Table_1_Form()
        glb.table_1_search = Table_1_Search()
        glb.login = Login(glb.user_list) # create (hidden) login window

    if not "enable here to run global event filter during development":
        """enable above to see in terminal ~many~ (almost all) events occuring in the application,
        including events in class instances and children widgets.
        The events pass thru the eventFilter() of an instance of MenuWindow()
        """
        qApp.installEventFilter(MenuWindow())        #pylint: disable = undefined-variable

    if "Open Main Menu window":
        glb.menu_win.show()

    # Note: __ini__ sections of above classes are run here last

    app.exec_()
    sys.exit()
