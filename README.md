# PERSONAL BLOG #

## 1. Develop ##

### 1.1. Backend ###

```bash
mkdir backend
cd backend
python3 -m venv venv
source venv/bin/active
pip3 install flask
```

### 1.2. Frontend ###

```bash
mkdir frontend
```

## 2. Install ##

### 2.1. Backend ###

```bash
pip3 install --upgrade -r requirements.txt
```

### 2.2. Frontend ###

```bash
cd ./frontend/personal_blog_spa
npm install
```

## 3. Manage database ##

```bash
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

You can use shell to modify db such as adding admin account

```bash
python3 manage.py shell
```

## 4. Run ##

## 4.1. Backend ##

```bash
python3 appserver.py
```

or

```bash
gunicorn --workers=2 -b 127.0.0.1:5000 appserver:app
```

## 4.2. Frontend ##

```bash
npm run dev
```
