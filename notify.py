import gi
try:
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    notify = True
except ImportError:
    notify = False


def notification():
    if not notify:
        return
    else:
        Notify.init("Workreport script")
        # Create the notification object and show once
        notifyme = Notify.Notification.new("The email for the workreport was sent successfully")
        notifyme.show()
        # Done using notifications
        Notify.uninit()

