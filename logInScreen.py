from Tkinter import *

# main root 
root = Tk()

# Set title of window and size
root.title("Conference Scheduler")
root.geometry("800x600")

# Add a username label and text entry field
Label(text='Username: ').place(x = 50,y = 10)
username1 = Entry(root, width=40)
username1.place(x=150, y=10)

# Add a password label and text entry field with hidden entry
Label(text='Password: ').place(x = 50,y = 60)
password1 = Entry(root,show = '*', width=40)
password1.place(x=150, y=60)

# Add a button for signing in
# TODO: Add functionality checking with database if username/pass combo is correct and make right move if it is.
signInButton = Button(root, text ="Sign In")
signInButton.configure(background = 'light gray')
signInButton.place(x = 150, y = 110)

# Add a button for signing up
# TODO: Add functionality to go to new screen and add data they enter and go to appropriate screen.
signUpButton = Button(root, text ="Sign Up")
signUpButton.configure(background = 'light gray')
signUpButton.place(x = 220, y = 110)



# Run it
mainloop()