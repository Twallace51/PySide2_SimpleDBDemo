"""Module providing basic database manipulation functions for a single table

The demo database 'test.db' used here is a simple sqlite3 database,  created with:

    CREATE TABLE "table_1" (
        "id"        INTEGER NOT NULL UNIQUE,
        "text_1"    TEXT DEFAULT "",
        "integer_1" INTEGER DEFAULT 0,
        "real_1"    REAL DEFAULT 0.0,
        "date_1"    TEXT DEFAULT '2020-03-14',
        PRIMARY KEY("id")
    );

The database also has representative data for editing, adding, deleting, filtering, printing   ....

"""
#p ylint: disable = fixme
#TODO

if __name__ == '__main__':
    """this ensures project starts properly from any module"""
    import _RUN_ME    # pylint: disable = unused-import

#pylint: disable = no-member, unused-import, ungrouped-imports, import-error
if 'imports':
    import sys
    import _support as glb
    from _support import(
        debug,
        debug_sql,
        notify_,
        confirm_,
        open_database,
        is_valid_date,
        )

    if "PySide2":
        import PySide2.QtGui as G
        import PySide2.QtSql as S
        import PySide2.QtCore as C
        import PySide2.QtWidgets as W
        import PySide2.QtPrintSupport as P
        from   PySide2.QtCore import Qt

if "customize module for a specific table":
    """following need to be updated for any table other than table_1 """

    def customize_table(win):
        """ """
        win.total_columns = 5
        win.headers = 'ID|Text_1|Integer_1|Real_1|Date_1'
        win.table.setColumnCount(win.total_columns)

        win.table.setColumnWidth(0, 60)
        win.table.setColumnWidth(1, 250)
        win.table.setColumnWidth(2, 100)
        win.table.setColumnWidth(3, 100)
        win.table.setColumnWidth(4, 100)

        win.table.setMinimumSize(180, 900)
        win.table.setHorizontalHeaderLabels(win.headers.split('|'))

    def get_table_1_count():
        """ """
        return """SELECT COUNT(*) FROM table_1 {} """.format(glb.table_1_list.filter_str)  # to get total database rows

    def get_table_1_rows():
        """ """
        return """SELECT id, text_1, integer_1, real_1, date_1 FROM table_1 {} """.format(glb.table_1_list.filter_str)

class Table_1_List(W.QWidget):         #pylint: disable = invalid-name
    """Data List class module
    Window shows full list,  or
    partial list, if was filtered by Search Form.

    Allows:
        showing a table from database as a list
        allows adding new row to list --> opens a blank form_window blank -> save/discard -> status messages
        allows search-filtering and sorting of list fields
        allows selecting one row from list by mouse click --> opens a form_window showing row in edit mode
        printing current (filtered) list data

 """
    def __init__(self):
        """ """
        W.QWidget.__init__(self)

        if "window attributes":
            self.setWindowTitle("List - click row to select ")
            self.setGeometry(glb.win_placement)

            self.setMinimumSize(160, 160)

        if "create toolbar actions":
            self.to_previous_win_act = W.QAction('Return to previous', self, shortcut='Ctrl+R')
            self.preview_act = W.QAction('Preview', self)
            self.print_act = W.QAction('Print', self, shortcut='Ctrl+P')
            self.about_app_act = W.QAction("Show List About box", self, shortcut="Ctrl+A")
            self.add_new_act = W.QAction("Add New to List", self)
            self.filter_like_act = W.QAction("Set Filters", self)
            self.remove_filters_act = W.QAction("Remove Filters", self)

        if "set action icons":
            self.to_previous_win_act.setIcon(G.QIcon(glb.icons + '/actions/go-previous.png'))
            self.preview_act.setIcon(G.QIcon(glb.icons + '/actions/document-print-preview.png'))
            self.print_act.setIcon(G.QIcon(glb.icons + '/actions/document-print.png'))
            self.about_app_act.setIcon(G.QIcon(glb.icons + '/actions/help-about.png'))
            self.add_new_act.setIcon(G.QIcon(glb.icons + '/actions/list-add-user.png'))
            self.filter_like_act.setIcon(G.QIcon(glb.icons + '/actions/view-filter.png'))
            self.remove_filters_act.setIcon(G.QIcon(glb.icons + '/actions/project-development-close.png'))

        if "set action connections":
            self.to_previous_win_act.triggered.connect(self.list_close_handler)
            self.preview_act.triggered.connect(self.handle_preview_handler)
            self.print_act.triggered.connect(self.handle_print_handler)
            self.about_app_act.triggered.connect(
                lambda: W.QMessageBox.about(self, "About Window class module", __doc__))
            self.add_new_act.triggered.connect(self.add_new_row_handler)
            self.filter_like_act.triggered.connect(self.open_filters_handler)
            self.remove_filters_act.triggered.connect(self.remove_filters_handler)

        if "toolbar setup":
            self.tool_bar = W.QToolBar(self)
            self.tool_bar.addAction(self.to_previous_win_act)
            self.tool_bar.addSeparator()
            self.tool_bar.addAction(self.about_app_act)
            self.tool_bar.addAction(self.preview_act)
            self.tool_bar.addAction(self.add_new_act)
            self.tool_bar.addSeparator()
            self.tool_bar.addAction(self.filter_like_act)
            self.tool_bar.addAction(self.remove_filters_act)

            self.tool_bar.setLayoutDirection(Qt.RightToLeft)

        if "default toolbar status":
            self.remove_filters_act.setEnabled(False)

        if "add tool_bar to window layout":
            self.window_layout = W.QGridLayout(self)
            self.setLayout(self.window_layout)
            self.window_layout.addWidget(self.tool_bar, 0, 0)

        if "create list table":
            self.table = W.QTableWidget(self)

        if "customize table":
            customize_table(self)

        if "add table to window layout":
            self.window_layout.addWidget(self.table, 1, 0)

        if "table click event connection":
            self.table.clicked.connect(self.current_cell)

    if "class methods":
        def current_cell(self):
            """ """
            # col = self.table.currentColumn()
            if "get data for row that was clicked":
                row = self.table.currentRow()
                glb.list_id = self.table.item(row, 0).text()
                self.current_cell_handler()

        def update_table_1_list(self):
            """new and updated records do not show,  unless window updated ..."""
            query_1 = S.QSqlQuery()
            if "get list data":
                query_1.exec_(get_table_1_count())
                if not query_1.isActive():
                    notify_("Error", "Invalid_query")
                    return
                query_1.first()
                total_rows = query_1.value(0)

            if "update table size":
                self.table.setRowCount(total_rows)

            if "place data in table ...":
                query_2 = S.QSqlQuery()
                query_2.exec_(get_table_1_rows())
                query_2.first()
                if not query_2.isActive():
                    notify_("Error", "Invalid_query")
                    return

                self.table.setSortingEnabled(False) # need to disable automatic sorting when filling table!

                for row in range(total_rows):
                    for col in range(self.total_columns):
                        item = W.QTableWidgetItem(str(query_2.value(col)))
                        if col != 1:
                            item.setTextAlignment(int(Qt.AlignCenter))
                        self.table.setItem(row, col, item)
                    query_2.next()
                self.table.sortItems(1, order=Qt.AscendingOrder)

                self.table.setSortingEnabled(True)

    if "print methods":

        def handle_print_handler(self):
            """ """
            dlg1 = P.QPrintDialog()
            if dlg1.exec_() == W.QDialog.Accepted:
                self.handle_paint_request(dlg1.printer())

        def handle_preview_handler(self):
            """ """
            self.hide()
            dlg1 = P.QPrintPreviewDialog()
            dlg1.paintRequested.connect(self.handle_paint_request)
            dlg1.exec_()
            self.show()

        def handle_paint_request(self, printer):
            """ """
            document = G.QTextDocument()
            cursor = G.QTextCursor(document)
            if "create format for table created below":
                format_table = G.QTextTableFormat()
                format_table.setCellPadding(0)
                format_table.setCellSpacing(0)

                format_table.setBorderStyle(G.QTextTableFormat.BorderStyle_None)
                format_table.setHeaderRowCount(0)  # value causes row(s) to be repeated across multiple pages ie headers
                format_table.setAlignment(Qt.AlignLeft)

            if "create table, format and add data":
                table = cursor.insertTable(self.table.rowCount(), self.table.columnCount(), format_table)  # pylint: disable = unused-variable
                for row in range(self.table.rowCount()):
                    for col in range(self.table.columnCount()):
                        cursor.insertText(self.table.item(row, col).text())
                        cursor.movePosition(G.QTextCursor.NextCell)

            document.print_(printer)

    if "window navigation handlers":

        def list_close_handler(self):
            """ """
            glb.menu_win.show()
            self.hide()

        def open_filters_handler(self):
            """ """
            self.hide()
            glb.table_1_search.show()

        def remove_filters_handler(self):
            """ """
            self.filter_str = ""
            self.remove_filters_act.setEnabled(False)
            self.update_table_1_list()

        def add_new_row_handler(self):
            """ """
            self.hide()
            glb.table_1_form.set_blank_form_mode()
            glb.table_1_form.show()

        def current_cell_handler(self):
            """show form window with selected data"""
            glb.table_1_form.show_table_1_data(glb.list_id)
            glb.table_1_form.set_update_form_mode()
            self.hide()
            glb.table_1_form.show()

    def closeEvent(self, event): #pylint: disable = invalid-name, unused-argument
        """
        sub classing W.QWidget function
        to return to previous window,  not to close app
        """
        self.list_close_handler()

class Table_1_Form(W.QWidget):         #pylint: disable = invalid-name
    """This window shows fields of one row in table,  allowing:
            update of fields
            deleting row
            adding a new row to table"""

    def __init__(self):
        W.QWidget.__init__(self)

        if "attributes":
            self.setWindowTitle("Data Form - click field to edit")
            self.setGeometry(glb.win_placement)
            self.setMinimumSize(160, 160)
            self.invalid_msg = None

        if "QActions":

            self.to_previous_win_act = W.QAction('Return to previous', self, shortcut='Ctrl+R')
            self.save_act = W.QAction("Save ...", self, enabled=True)
            self.cancel_act = W.QAction("Cancel ...", self, enabled=True)
            self.delete_row_act = W.QAction("Delete ...", self, enabled=True)
            self.about_app_act = W.QAction("Show the About box", self, shortcut="Ctrl+A")
            self.print_act = W.QAction('Print', self)

        if "action icons":

            self.to_previous_win_act.setIcon(G.QIcon(glb.icons + '/actions/go-previous.png'))
            self.save_act.setIcon(G.QIcon(glb.icons + '/actions/document-save.png'))
            self.cancel_act.setIcon(G.QIcon(glb.icons + '/actions/edit-undo.png'))
            self.delete_row_act.setIcon(G.QIcon(glb.icons + '/actions/edit-delete.png'))
            self.about_app_act.setIcon(G.QIcon(glb.icons + '/actions/help-about.png'))
            self.print_act.setIcon(G.QIcon(glb.icons + '/actions/document-print.png'))

        if "action connections":

            self.to_previous_win_act.triggered.connect(self.close)
            #self.save_act -  connected below for addnew or update case
            self.cancel_act.triggered.connect(self.cancel_update)
            self.delete_row_act.triggered.connect(self.delete_row)
            self.about_app_act.triggered.connect(
                lambda: W.QMessageBox.about(self, "About Window class module", __doc__))
            self.print_act.triggered.connect(self.print_form)

        if "toolbar":

            self.tool_bar = W.QToolBar(self)
            self.tool_bar.addAction(self.to_previous_win_act)
            self.tool_bar.addAction(self.about_app_act)
            self.tool_bar.addAction(self.print_act)
            self.tool_bar.addAction(self.cancel_act)
            self.tool_bar.addAction(self.save_act)
            self.tool_bar.addAction(self.delete_row_act)

            self.tool_bar.setLayoutDirection(Qt.RightToLeft)

        if "default toolbar status":
            self.save_act.setEnabled(False)
            self.cancel_act.setEnabled(False)
            self.delete_row_act.setEnabled(False)

        if "window layout":
            self.window_layout = W.QGridLayout(self)

            if "add toolbar":
                self.window_layout.addWidget(self.tool_bar, 0, 0)
                self.setLayout(self.window_layout)

            if "header setup":
                self.header = W.QLabel()
                self.header.setFont(G.QFont("Times", 15, G.QFont.Bold))

            if "form setup":
                self.form_layout = W.QFormLayout()
                self.form_groupbox = W.QGroupBox()
                self.form_groupbox.setLayout(self.form_layout)
                self.form_groupbox.setFont(G.QFont("Times", 15))

            if "add widgets to window layout":
                self.window_layout.addWidget(self.header, 1, 0)
                self.window_layout.addWidget(self.form_groupbox, 2, 0)

            if "add calendar":
                self.cal01 = W.QCalendarWidget(self)
                self.window_layout.addWidget(self.cal01, 3, 0)
                self.cal01.hide()

            if "push all widgets up":
                self.window_layout.setRowStretch(4, 100)

        if "form widgets":
            self.led01 = W.QLineEdit(self)    # TEXT
            self.led02 = W.QLineEdit(self)    # INTEGER
            self.led03 = W.QLineEdit(self)    # REAL
            self.led04 = W.QLineEdit(self)    # DATE yyyy-MM-dd

        if "form layout":
            self.form_layout.addRow('Text:   ', self.led01)
            self.form_layout.addRow('Integer:', self.led02)
            self.form_layout.addRow('Real:   ', self.led03)
            self.form_layout.addRow('Date:   ', self.led04)

        if "install local event filter":
            """for individual widgets,  connect to local eventFilter (see below) """
            self.led01.installEventFilter(self) # works,  but only on led01
            self.led02.installEventFilter(self) # works,  but only on led02
            self.led03.installEventFilter(self) # works,  but only on led03
            self.led04.installEventFilter(self) # works,  but only on led04

    if "QAction handlers":
        def close(self):
            """ """
            glb.table_1_list.show()
            self.hide()

        def delete_row(self):
            """ """
            if confirm_("Update:"):
                sql_str = """DELETE FROM table_1 WHERE id = "{}" """.format(glb.list_id)

                query = S.QSqlQuery()
                query.exec_(sql_str)
                query.first()

                notify_("Delete:", "Row was deleted")
                glb.menu_win.show()
                self.hide()

            else:
                notify_("Delete:", "Delete row was canceled")

        def print_form(self):
            """ """
            if confirm_("Print Screen:"):
                printer = P.QPrinter()
                painter = P.G.QPainter()
                painter.begin(printer)
                screen = self.grab() # to print whole window
                painter.drawPixmap(10, 10, screen)
                painter.end()

        def insert_new_row(self):
            """ """
            if self.validate_data():
                if self.confirm_update():
                    sql_str = """INSERT INTO table_1 VALUES
                        ("{}","{}", "{}", "{}", "{}") """.format(
                            glb.list_id,
                            self.led01.text(),
                            self.led02.text(),
                            self.led03.text(),
                            self.led04.text())
                    query = S.QSqlQuery()
                    query.exec_(sql_str)
                    query.first()

                else:
                    notify_("Save Canceled", "Any input was discarded")
                    self.cancel_add()

                self.set_default_form_mode()

                glb.menu_win.show()
                glb.table_1_list.hide()
                self.hide()
            else:
                notify_("Data Invalid:", self.invalid_msg)

        def cancel_add(self):
            """ """
            notify_("Canceled", "New row was discarded")
            self.set_default_form_mode()
            self.hide()
            glb.table_1_list.show()

        def cancel_update(self):
            """ """
            notify_("Save Canceled", "Any updates were discarded")
            glb.table_1_list.show()
            self.set_default_form_mode()
            self.hide()

        def save_update(self):
            """ """
            if self.validate_data():
                """ save updated data back to db """
                if confirm_("Update"):
                    self.update_data(glb.list_id)
                    notify_("Saved", "Updates were saved")
                    self.set_default_form_mode()
                    glb.form_win.hide()
                    glb.table_1_list.hide()
                    glb.menu_win.show()
                else:
                    notify_("Save canceled:", "Updates discarded")
                    self.cancel_update()
            else:
                notify_("Invalid_input:", self.invalid_msg)

    if "class methods":

        def validate_data(self):  # boolean return
            """ """
            self.invalid_msg = None
            if "test for blank entries":
                if self.led01.text() == '':
                    self.invalid_msg = 'Text  can not be blank'  # required > '' or not None
                    self.led01.setFocus()
                elif self.led02.text() == '':
                    self.invalid_msg = 'Integer can not be blank'  # required > '' or not None
                    self.led02.setFocus()
                elif self.led03.text() == '':
                    self.invalid_msg = 'Real can not be blank'
                    self.led03.setFocus()
                elif self.led04.text() == '':
                    self.invalid_msg = 'Date can not be blank'
                    self.led04.setFocus()

            if self.invalid_msg:
                return False

            if "test for integer type":
                try:
                    int(self.led02.text())
                except ValueError:
                    self.invalid_msg = 'entry must be integer'
                    self.led03.setFocus()
                    return False

            if "test for decimal type":
                try:
                    float(self.led03.text())
                except ValueError:
                    self.invalid_msg = 'entry must be integer or decimal'
                    return False

            if not is_valid_date(self.led04.text()):
                self.invalid_msg = 'date ' + self.led04.text() + ' invalid'
                return False

            return True

        if "update current record methods":

            def show_table_1_data(self, list_id_parameter):
                """following correct for table_1,   update for a different table """
                self.form_groupbox.setTitle("ID: "+ str(list_id_parameter))
                sql_str = """SELECT * FROM table_1 WHERE id = {}""".format(str(list_id_parameter))

                query = S.QSqlQuery()
                query.exec_(sql_str)
                if not query.isActive():
                    notify_("Invalid Query", sql_str)
                    return
                query.first()

                self.led01.setText(str(query.value(1)))
                self.led02.setText(str(query.value(2)))
                self.led03.setText(str(query.value(3)))
                self.led04.setText(str(query.value(4)))

            def update_data(self, list_id_parameter):
                """following correct for table_1,   update for a different table """
                #pylint: disable = no-self-use
                sql_str = """UPDATE table_1 SET
                    text_1 = "{}",
                    integer_1 = "{}",
                    real_1 = "{}",
                    date_1 = "{}"
                    WHERE id = {} """.format(
                        self.led01.text(),
                        self.led02.text(),
                        self.led03.text(),
                        self.led04.text(),
                        str(list_id_parameter),
                        )
                query = S.QSqlQuery()
                query.exec_(sql_str)

            def update_date(self):
                """ """
                self.led04.setText(self.cal01.selectedDate().toString(Qt.ISODate))
                self.cal01.selectionChanged.disconnect(self.update_date)
                self.cal01.hide()

        if "set form modes":

            def set_blank_form_mode(self):
                """ """
                if "configure toolbar icons for adding ":
                    self.to_previous_win_act.setEnabled(False)
                    self.print_act.setEnabled(False)
                    self.delete_row_act.setEnabled(False)

                    self.cancel_act.setEnabled(True)
                    self.save_act.setEnabled(True)

                if "configure triggers":
                    self.save_act.triggered.disconnect()
                    self.cancel_act.triggered.disconnect()
                    self.save_act.triggered.connect(self.insert_new_row)
                    self.cancel_act.triggered.connect(self.cancel_add)

                if "find next id":
                    sql_str = "SELECT  MAX(id) FROM table_1"
                    query = S.QSqlQuery()
                    query.exec_(sql_str)
                    query.first()
                    glb.list_id = str(int(query.value(0))+1)

                if "setup blank form - show and wait":
                    self.header  = ""
                    self.form_groupbox.setTitle("ID: " + glb.list_id)

                    self.led01.setText('')
                    self.led02.setText('0')
                    self.led03.setText('0.0')
                    self.led04.setText('')
                    self.show()

            def set_default_form_mode(self):
                """  """
                self.save_act.setEnabled(False)
                self.cancel_act.setEnabled(False)

                self.delete_row_act.setEnabled(True)
                self.to_previous_win_act.setEnabled(True)
                self.print_act.setEnabled(True)

            def set_update_form_mode(self):
                """ """
                if "configure toolbar icons for updates":
                    self.to_previous_win_act.setEnabled(True)
                    self.cancel_act.setEnabled(False)
                    self.save_act.setEnabled(False)
                    self.delete_row_act.setEnabled(True)

                if "configure triggers for updates":
                    self.cancel_act.triggered.disconnect()
                    self.save_act.triggered.disconnect()
                    self.cancel_act.triggered.connect(self.cancel_update)
                    self.save_act.triggered.connect(self.save_update)

    if "sub classed QWidget methods":
        """do not change names of following subclassed methods ... """
        #pylint: disable = invalid-name, unused-argument

        def eventFilter(self, obj, event):
            """ subclassed QWidget function - by default simply returns False  """
            # pylint: disable = invalid-name
            if event.type() == C.QEvent.MouseButtonRelease or event.type() == C.QEvent.KeyRelease:
                if obj in (self.led01, self.led02, self.led03, self.led04):

                    if "hide calendar widget":
                        self.cal01.hide()
                    if "reset toolbar to edit mode":
                        self.save_act.setEnabled(True)
                        self.cancel_act.setEnabled(True)
                        self.delete_row_act.setEnabled(False)
                        self.print_act.setEnabled(False)
                        self.to_previous_win_act.setEnabled(False)

                if obj is self.led04: # show calendar widget
                    if "show calendar widget":
                        self.cal01.selectionChanged.connect(self.update_date)
                        self.cal01.show()

            return False  # passes all events from object -> parent

        def closeEvent(self, event):  #pylint: disable = invalid-name, unused-argument
            """ exits app by default """
            self.close()

class Table_1_Search(W.QWidget):       #pylint: disable = invalid-name
    """This window allows:
            searching for one or more partial strings in table list,  using the SQL LIKE command.
            clicking on a filtered row and opening it in a form window
    """
    def __init__(self):
        W.QWidget.__init__(self)

        if "attributes":
            self.setWindowTitle("Search Form")
            self.setGeometry(glb.win_placement)
            self.setMinimumSize(160, 160)

        if "QActions":

            self.about_form_act = W.QAction("Info", self, shortcut="Ctrl+A")
            self.cancel_act = W.QAction("Cancel", self, shortcut="Ctrl+A")
            self.blank_form_act = W.QAction("Blank fields", self, shortcut="Ctrl+A")
            self.run_search_act = W.QAction("Run search", self, shortcut="Ctrl+A")

        if "set action icons":
            self.about_form_act.setIcon(G.QIcon(glb.icons + '/actions/help-about.png'))
            self.cancel_act.setIcon(G.QIcon(glb.icons + '/actions/edit-undo.png'))
            self.blank_form_act.setIcon(G.QIcon(glb.icons + '/actions/archive-remove.png'))
            self.run_search_act.setIcon(G.QIcon(glb.icons + '/actions/edit-find-user.png'))

        if "set connections":

            self.about_form_act.triggered.connect(
                lambda: W.QMessageBox.about(self, "Search Info", Table_1_Search.__doc__))
            self.cancel_act.triggered.connect(self.cancel_handler)
            self.blank_form_act.triggered.connect(self.blank_table_1_form_handler)
            self.run_search_act.triggered.connect(self.run_search_handler)

        if "update toolbar":
            self.tool_bar = W.QToolBar(self)
            self.tool_bar.addAction(self.cancel_act)
            self.tool_bar.addAction(self.about_form_act)
            self.tool_bar.addAction(self.blank_form_act)
            self.tool_bar.addAction(self.run_search_act)

            self.tool_bar.setLayoutDirection(Qt.RightToLeft)

        if "add tool_bar to window layout":
            self.window_layout = W.QGridLayout(self) # or should be another,  QVBoxLayout?
            self.setLayout(self.window_layout)
            self.window_layout.addWidget(self.tool_bar, 0, 0)

        if "groupbox setup":
            self.form_layout = W.QFormLayout()
            self.form_groupbox = W.QGroupBox()
            self.form_groupbox.setLayout(self.form_layout)
            self.form_groupbox.setFont(G.QFont("Times", 15))
            self.window_layout.addWidget(self.form_groupbox, 2, 0)

        if "form widgets":
            self.led05 = W.QLineEdit(self)    # integer
            self.led01 = W.QLineEdit(self)    # TEXT
            self.led02 = W.QLineEdit(self)    # INTEGER
            self.led03 = W.QLineEdit(self)    # REAL
            self.led04 = W.QLineEdit(self)    # DATE yyyy-MM-dd

        if "form layout":
            self.form_layout.addRow('ID:     ', self.led05)  #TODO   should be lable,  not led ?
            self.form_layout.addRow('Text:   ', self.led01)
            self.form_layout.addRow('Integer:', self.led02)
            self.form_layout.addRow('Real:   ', self.led03)
            self.form_layout.addRow('Date:   ', self.led04)

    if "handlers":
        #pylint: disable = missing-docstring
        def cancel_handler(self):
            glb.table_1_list.show()
            self.hide()

        def run_search_handler(self):
            """following needs to be updated for table other than table_1 """
            glb.table_1_list.filter_str = self.create_table_1_where()
            if not glb.table_1_list.filter_str:
                notify_("Empty filter string")
                return
            if "get list data":
                str_sqlcount = """SELECT COUNT(*) FROM table_1 {} """.format(glb.table_1_list.filter_str)  # to get total database rows
                query_1 = S.QSqlQuery()
                query_1.exec_(str_sqlcount)
                query_1.first()
                total_rows = query_1.value(0)
                if not query_1.isActive():
                    notify_("Invalid Query", str_sqlcount)
                    return
                if not total_rows:
                    notify_("Empty Query", str_sqlcount)
                    return

            if "update table size":
                glb.table_1_list.table.setRowCount(total_rows)

            if "place data in table ...":
                glb.table_1_list.table.setSortingEnabled(False)
                #Note: need to turn sorting off while folling table,  or data gets scrambled !!!
                str_sqldata = """SELECT id, text_1, integer_1, real_1, date_1 FROM table_1 {} """.format(glb.table_1_list.filter_str)
                query_2 = S.QSqlQuery()
                query_2.exec_(str_sqldata)
                query_2.first()

                for row in range(total_rows):
                    for col in range(glb.table_1_list.total_columns):
                        item = W.QTableWidgetItem(str(query_2.value(col)))
                        if col != 1:
                            item.setTextAlignment(int(Qt.AlignCenter))
                        glb.table_1_list.table.setItem(row, col, item)
                    query_2.next()


            glb.table_1_list.table.sortItems(1, order=Qt.AscendingOrder)
            glb.table_1_list.table.setSortingEnabled(True)

            glb.table_1_list.show()
            self.hide()

        def create_table_1_where(self):
            """following needs to be updated for table other than table_1 """
            tmp = ""
            if self.led01.text():
                tmp = " {} LIKE '%{}%' ".format("text_1", self.led01.text())
            if self.led02.text():
                if tmp:
                    tmp = tmp + " AND  {} LIKE '%{}%' ".format("integer_1", self.led02.text())
                else:
                    tmp = " {} LIKE '%{}%' ".format("integer_1", self.led02.text())
            if self.led03.text():
                if tmp:
                    tmp = tmp + " AND {} LIKE '%{}%' ".format("decimal_1", self.led03.text())
                else:
                    tmp = " {} LIKE '%{}%' ".format("decimal_1", self.led03.text())
            if self.led04.text():
                if tmp:
                    tmp = tmp + " AND {} LIKE '%{}%' ".format("date_1", self.led04.text())
                else:
                    tmp = " {} LIKE '%{}%' ".format("date_1", self.led04.text())
            if self.led05.text():
                if tmp:
                    tmp = tmp + " AND {} LIKE '{}' ".format("id", self.led05.text())
                else:
                    tmp = " {} LIKE '{}' ".format("id", self.led05.text())

            if tmp:
                glb.table_1_list.remove_filters_act.setEnabled(True)
                return "WHERE " + tmp
            glb.table_1_list.remove_filters_act.setEnabled(False)
            return ''


        def blank_table_1_form_handler(self):
            self.led01.setText("")
            self.led02.setText("")
            self.led03.setText("")
            self.led04.setText("")
            self.led05.setText("")
            glb.table_1_list.remove_filters_act.setEnabled(False)
