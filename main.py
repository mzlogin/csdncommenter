import CsdnHandler

def main():
    csdn = CsdnHandler.CsdnHandler()
    while csdn.login() is False:
        print 'Login failed! Please try again.'
    print 'Login succeed!'

    csdn.autoComment()

if __name__ == '__main__':
    main()
