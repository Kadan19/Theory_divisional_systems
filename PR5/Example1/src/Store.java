 class Store {
    private int product = 0;
    public synchronized void get()
    {
        while (product < 1)
        {
            try
            {
                wait();
            }
            catch (InterruptedException e)
            {
            }
        }
        product--;
        System.out.println("Покупець купив 1 товар");
        System.out.println("Товарiв на складi: " + product);
        notify();
    }

    public synchronized void put()
    {

        while (product >= 3)
        {
            try
            {
                wait();
            }

            catch (InterruptedException e)
            {

            }
        }
        product++;
        System.out.println("Виробник додав 1 товар");
        System.out.println("Товарiв на складi: " + product);
        notify();
    }
}