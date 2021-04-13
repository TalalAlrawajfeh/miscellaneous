package pool.thread;

import pool.ObjectPool;

import static pool.thread.ThreadStatus.*;

/**
 * Created by u624 on 5/7/17.
 */
public class AutoReleasableThread extends Thread {
    private final Object monitor = new Object();
    private ObjectPool<AutoReleasableThread> threadPool;
    private ThreadStatus threadStatus;
    private Runnable operation;

    public AutoReleasableThread(ObjectPool<AutoReleasableThread> threadPool) {
        this.threadPool = threadPool;
        this.threadStatus = WAITING;
    }

    public void doOperation(Runnable operation) {
        synchronized (monitor) {
            this.operation = operation;
            this.threadStatus = RUNNING;
            monitor.notifyAll();
        }
    }

    @Override
    public void run() {
        synchronized (monitor) {
            do {
                if (WAITING == threadStatus) {
                    try {
                        monitor.wait();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
                if (RUNNING == threadStatus) {
                    operation.run();
                    threadPool.release(this);
                    this.threadStatus = WAITING;
                }
                if (SHUTDOWN == threadStatus) {
                    break;
                }
            } while (true);
        }
    }

    public void shutdown() {
        synchronized (monitor) {
            threadStatus = SHUTDOWN;
            monitor.notifyAll();
        }
    }
}
