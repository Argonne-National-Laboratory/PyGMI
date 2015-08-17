from PySide.QtGui import QPlainTextEdit

#future update
#This class provides a text editor deriving from Qt QPlainTextEdit
#where an input form is automatically generated when the user double clicks on a line in the text editor.
#By analyzing the content of the line, the class automatically generates a form  which contains input boxes for each parameter expected on that line.
#The user can thus specify in that form the value they want for each parameter, then press OK (or Cancel)
#which will (or will not) rewrite that line in the sequence editor.

class MyMacroEdit(QPlainTextEdit):
    def __init__(self,*args,**kwargs):
        QPlainTextEdit.__init__(self,*args,**kwargs)
#for future update
##    def mouseDoubleClickEvent(self,event):
##        QPlainTextEdit.mouseDoubleClickEvent(self,event)
##        if event.button()==Qt.MiddleButton:
##            cursor=self.textCursor()
##            txt=cursor.block().text()
##            form=My_Form_for_sequence_editor(form_string=txt)
##            if form.dialog_needed:
##                if form.exec_():
##                    cursor.select(cursor.BlockUnderCursor)
##                    cursor.removeSelectedText()
##                    self.insertPlainText('\n'+form.user_string)
##            else:
##                form.done(1)
##                #print "no form was needed"

#for future update 
##class My_Form(QDialog):
##    def __init__(self, parent=None,form_string=None):
##        super(My_Form, self).__init__(parent)
##        self.setWindowTitle(u'Please enter parameters values')
##        #analyze string
##        placeholders="(FLOAT|LETTER|INTEGER|MESSAGE|FILE|DIRECTORY)"
##        my_expression=QRegExp(placeholders)
##        #check if the line of text contains some input parameters
##        index = my_expression.indexIn(form_string)
##        if index != -1:#at least one parameter found, a form is needed
##            self.dialog_needed=True
##            #formLayout = QFormLayout()
##            formLayout = QHBoxLayout()
##            self.labels=[]
##            self.widgets=[]
##            #loop on all the parameters that can be captured
##            working_string=form_string
##            while my_expression.indexIn(working_string)!=-1:
##                lab=working_string[:my_expression.pos(1)]
##                widg=QLineEdit(my_expression.cap(1))
##                self.labels.append(lab)
##                self.widgets.append(widg)
##                # Create widgets
##                #formLayout.addRow(lab,widg)
##                formLayout.addWidget(QLabel(lab))
##                formLayout.addWidget(widg)
##                working_string=working_string[my_expression.pos(1)+len(my_expression.cap(1)):]
##            #add last part of the string
##            #formLayout.addRow(QLabel(working_string))
##            formLayout.addWidget(QLabel(working_string))
##            #add two buttons
##            self.button_OK = QPushButton("OK")
##            self.button_Can = QPushButton("Cancel")
##            #formLayout.addRow(self.button_OK,self.button_Can)
##            formLayout.addWidget(self.button_OK)
##            formLayout.addWidget(self.button_Can)
##            # Set dialog layout
##            self.setLayout(formLayout)
##            # Add button signal to slot
##            self.button_OK.clicked.connect(self.values_entered)
##            self.button_Can.clicked.connect(self.reject)
##            self.working_string=working_string
##        else:
##            #print "just go on 0"
##            self.dialog_needed=False
##            self.user_string=form_string
##            #print "just go on"
##            
##    def values_entered(self):
##        self.user_string=u''
##        for i in range(len(self.labels)):         
##            self.user_string+=self.labels[i]+self.widgets[i].text()
##        self.user_string+=self.working_string
##        self.accept() 
 
                    
#if __name__ == "__main__":
    #import sys
    #app = QApplication(sys.argv)
    #window = Macro_editor(app)
    #window.show()
    #sys.exit(app.exec_())
