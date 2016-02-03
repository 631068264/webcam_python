<<<<<<< HEAD
# 使用说明



## 安装依赖
```
pip install -r requirements.txt
```


## 编码规范
编码需要符合pep8标准，不是为了啥，只是至少大家写出来的代码至少看起来像同一个人写的。

编码规范：[PEP 0008 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

Git服务器已经加了pep8检查，不符合规范的push会reject。
所以本地开发最好加上git-hook，加一个`pre-commit`即可。 [git-hook](https://github.com/cedricporter/pep8-git-hook)


## Git使用规范

仅仅使用develop分支，自己请在自己的分支上面开发。使用简化的[Git Flow](https://ihower.tw/blog/archives/5140)。

```
# 建立自己的分支
# 创建login分支进行login功能开发
(master) $ git checkout develop
(develop) $ git checkout -b feature/login

# 开发工作中，合并后别人的内容
(feature/login) $ git fetch && git rebase origin/develop

# 完成功能开发，合并到develop （注意：下面几步需要连续完成。不要做了一半去喝咖啡回来再做）
# 1.
(feature/login) $ git fetch && git rebase origin/develop
# 2.
(feature/login) $ git checkout develop
(develop) $ git pull --rebase
(develop) $ git merge feature/login
(develop) $ git push
```

### 有用的alias
```
# 查看分支与提交情况
alias gl='git log --color --graph --pretty=format:'\''%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'\'' --abbrev-commit --'
# 拉取远程
alias grb='git fetch && git rebase origin/develop'
```

## 测试开发的时候运行
去相应的项目目录，运行`python wsgi_handler.py`。

默认是启动调试模式，只要保存文件，就会自动reload代码。

默认端口5000。
=======
Hello webcam
>>>>>>> 3be8052baa33dc4e8783d1c4dcd44cce737287f1
