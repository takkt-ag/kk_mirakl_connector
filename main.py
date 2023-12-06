import sys
import connector.orders_acceptor

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--health-check':
        sys.exit()

    connector.orders_acceptor.accept_mirakl_orders()
