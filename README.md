# echo-redbox


Setup
===

First, install Python dependencies:

```sh
pip install -r requirements.txt
```

On mac, you may need to use a VirtualEnv, or install to your user's python library:
```sh
pip install --user -r requiements.txt
```


You will need to install phantomjs, this can be done on mac with:

```sh
brew install phantomjs
```

Use the following to install phantomjs on Ubuntu

```sh
apt-get install node nodejs-legacy npm
npm -g install phantomjs
```

Running
===

To start mysql, run:

```sh
docker-compose up
```

You can run docker-compose in detach mode so that it runs in the background like so:

```sh
docker-compose up -d
```


