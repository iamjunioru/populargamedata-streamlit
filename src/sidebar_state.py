
sidebar_state = "collapsed"

def toggle_sidebar_state():
    global sidebar_state
    sidebar_state = "collapsed" if sidebar_state == "auto" else "auto"
