package pool;

import exceptions.PoolException;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import static pool.PoolObjectStatus.AVAILABLE;
import static pool.PoolObjectStatus.TAKEN;

/**
 * Created by u624 on 5/6/17.
 */
public abstract class BlockingObjectPool<T> implements ObjectPool<T> {
    private static final int DEFAULT_POOL_SIZE = 10;
    private static final String EXPECTED_AVAILABLE_OBJECT = "Expected an available object in pool";
    private final Object poolMonitor = new Object();

    private int poolSize;
    private int takenObjectsCount = 0;
    private Map<T, PoolObjectStatus> pool = new HashMap<>();

    public BlockingObjectPool() {
        this.poolSize = DEFAULT_POOL_SIZE;
    }

    public BlockingObjectPool(int poolSize) {
        this.poolSize = poolSize;
    }

    @Override
    public T take() {
        synchronized (poolMonitor) {
            while (poolSize == takenObjectsCount) {
                try {
                    poolMonitor.wait();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            T object = poolSize == pool.size() ? pool.entrySet()
                    .stream()
                    .filter(e -> AVAILABLE == e.getValue())
                    .findAny()
                    .orElseThrow(() -> new PoolException(EXPECTED_AVAILABLE_OBJECT))
                    .getKey() : createObject();
            pool.put(object, TAKEN);
            takenObjectsCount++;
            return object;
        }
    }

    @Override
    public void release(T t) {
        synchronized (poolMonitor) {
            pool.put(t, PoolObjectStatus.AVAILABLE);
            takenObjectsCount--;
            poolMonitor.notifyAll();
        }
    }

    @Override
    public void closeAllResources() {
        pool.entrySet()
                .stream()
                .map(Entry::getKey)
                .forEach(this::destroyObject);
    }

    protected abstract T createObject();

    protected abstract void destroyObject(T t);
}
