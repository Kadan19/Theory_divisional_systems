﻿using ConsoleApp1;

class Program
{
    static void Main(string[] args)
    {
        int carCount = 5;

        Random random = new Random();
        Console.WriteLine("\tGO)!!");

        var fuelStation = new FuelStationMonitor(2, 300);
        var tasks = new Task[carCount];

        for (int i = 0; i < carCount; i++)
        {
            var car = new Car("car" + (i + 1), fuelStation, 100, random.Next(1, 5));
            tasks[i] = new Task(car.Run);
        }


        tasks.ToList().ForEach(x => x.Start());
        Thread.Sleep(30000);
        fuelStation.Fill(2000);
        Task.WaitAll(tasks);
        Console.WriteLine("\tFINISH!!!");
    }
}

namespace ConsoleApp1
{
    class FuelstationSemaphore : AbstractFuelstation
    {
        private Mutex mutex = new Mutex();
        private SemaphoreSlim semaphore;

        public FuelstationSemaphore(int columnCount, int reserve = 1000) :
        base(columnCount, reserve)
        {
            semaphore = new SemaphoreSlim(СolumnCount, СolumnCount);

        }

        public override void Fill(int amount)
        {
            mutex.WaitOne();
            if (amount + Reserve > Capacity)
                Reserve = Capacity;
            else
                Reserve += Capacity;
            Console.WriteLine("STATION TANK REFUELED");
            mutex.ReleaseMutex();
        }

        public override bool TryRefuel(Car car, int volume)
        {
            semaphore.Wait();
            mutex.WaitOne();
            bool result = false;
            if (volume <= Reserve)
            {

                Console.WriteLine($"Fuels reserve is {Reserve}. {volume} liters fueling began for {car.Name}");
                Reserve -= volume;
                mutex.ReleaseMutex();
                Thread.Sleep(100 * volume);
                Console.WriteLine($"{car.Name} fueling finished");
                result = true;

            }

            else

            {
                Console.WriteLine($"Fuel reserve {Reserve} is insufficient for {car.Name}");
                mutex.ReleaseMutex();

            }

            semaphore.Release();

            return result;
        }
    }


}


namespace ConsoleApp1
{
    class FuelStationMonitor : AbstractFuelstation
    {


        private object lockObject;
        private int freeColummCount;

        public FuelStationMonitor(int columnCount, int reserve) :
        base(columnCount, reserve)
        {
            lockObject = new object();
            freeColummCount = СolumnCount;

        }

        public override void Fill(int amount)
        {
            lock (lockObject)
            {
                if (amount + Reserve > Capacity)
                    Reserve = Capacity;
                else
                    Reserve += Capacity;
                Console.WriteLine("STATION TANK REFUELED");
                Monitor.PulseAll(lockObject);
            }
        }



        public override bool TryRefuel(Car car, int volume)
        {

            bool result = false;

            lock (lockObject)
            {
                while (freeColummCount <= 0)
                    Monitor.Wait(lockObject);
                if (volume <= Reserve)
                {
                    freeColummCount--;
                    Console.WriteLine($"Fuels reserve is {Reserve}. {volume}  liters fueling began for {car.Name} ");
                    Reserve -= volume;
                    result = true;
                }
                else
                {
                    Console.WriteLine($"fuel reserve {Reserve} is insufficient for {car.Name}");
                }
            }

            if (result)
            {
                Thread.Sleep(100 * volume);
                Console.WriteLine($"{car.Name} fueling finished");
                lock (lockObject)
                {

                    freeColummCount++;
                    Monitor.PulseAll(lockObject);

                }
            }

            return result;
        }
    }
}


namespace ConsoleApp1
{
    class Car
    {
        private static Random random = new Random();
        public string Name { get; set; }
        public int Tankvolume { get; }
        public AbstractFuelstation Station { get; }
        public int Refuelcount { get; }

        public Car(string name, AbstractFuelstation station, int tankVolume, int refuelCount)
        {

            Name = name;

            Tankvolume = tankVolume;

            Station = station;
            Refuelcount = refuelCount;
        }

        public void Run()
        {
            Console.WriteLine($"{Name} STARTED; refuel count is {Refuelcount}");
            for (int i = 0; i < Refuelcount; i++)
            {
                var volume = random.Next(Tankvolume) + 1;
                Console.WriteLine($"{Name} tries to get {volume} lit. for (i + 1) times");
                while (!Station.TryRefuel(this, volume))
                {
                    Console.WriteLine($"{Name} is waiting");
                    Thread.Sleep(random.Next(1, 5) * 1000);

                    Thread.Sleep(random.Next(1, 3) * 1000);
                    Console.WriteLine($"{Name} left the station for {i + 1} times");

                    Console.WriteLine($"{Name} SAID GOOD-BYE");
                }
            }
        }
    }
}


namespace ConsoleApp1
{
    abstract class AbstractFuelstation
    {
        public int Reserve { get; protected set; }
        public int Capacity { get; } = 1000;
        public int СolumnCount { get; }

        public AbstractFuelstation(int columnCount, int reserve = 1000)

        {
            if (columnCount <= 0) throw new Exception("Invalid column count");
            if (reserve > Capacity || reserve < 0) throw new Exception("Invalid reserve");
            СolumnCount = columnCount;
            Reserve = reserve;

        }
        public abstract void Fill(int amount);

        public abstract bool TryRefuel(Car car, int volume);
    }
}
