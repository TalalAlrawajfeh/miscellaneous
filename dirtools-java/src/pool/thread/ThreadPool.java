package pool.thread;

import pool.BlockingObjectPool;

/**
 * Created by u624 on 5/7/17.
 */
public class ThreadPool extends BlockingObjectPool<AutoReleasableThread> {
    public ThreadPool() {
        super();
    }

    public ThreadPool(int poolSize) {
        super(poolSize);
    }

    @Override
    protected AutoReleasableThread createObject() {
        AutoReleasableThread autoReleasableThread = new AutoReleasableThread(this);
        autoReleasableThread.start();
        return autoReleasableThread;
    }

    @Override
    protected void destroyObject(AutoReleasableThread autoReleasableThread) {
        autoReleasableThread.shutdown();
    }
}
