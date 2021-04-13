package pool;

/**
 * Created by u624 on 5/6/17.
 */
public interface ObjectPool<T> {
    T take();

    void release(T t);

    void closeAllResources();
}
