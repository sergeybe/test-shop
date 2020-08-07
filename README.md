# Shop

1. Create Python virtual environment and install developers packages:

```shell
mkvirtualenv test-shop -p `which python3`
pip install -r requirements-dev.txt
```

2. Run command to build Docker images and launch all of them:

```shell
make build start
```

3. Open url http://127.0.0.1/admin by browser.

4. Sign in as super user with login `demo` and password `demo` and add products to shop.

Note: 80 and 443 ports will be used by shop site and should be free before running.
