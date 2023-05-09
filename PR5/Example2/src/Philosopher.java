import java.util.concurrent.Semaphore;

    class Philosopher extends Thread 
    {
        Semaphore sem;

        int num =0;

        int id;


        Philosopher(Semaphore sem, int id) {

            this.sem = sem;
            this.id = id;
        }

        public void run()

        {
            try
            {
                while(num<3)
                {

                    sem.acquire();
                    System.out.println ("Фiлософ " + id+ " сiдає за стiл");

                            sleep(500) ;
                    num++;
                    System.out.println ("Фiлософ "  + id+ " встає зi столу");
                    sem.release();

                    sleep(500);
                }
            }
            catch(InterruptedException e)
            {
                System.out.println ("У фiлософа " + id + " проблеми зi здоров'ям");
            }
        }
    }