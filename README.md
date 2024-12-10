
ссылка на телеграмм бота: https://t.me/bank_rate_bot 

ссылка на dockerhub :https://hub.docker.com/r/avasilevskij/bank

Описание бота: телеграмм бот предназначен для просмотра актуальных курсов валют и цен на драгоценные металлы предоставляемые Национальным банком Республики Беларусь(https://www.nbrb.by)

Описание функций:   

                    "/cod  Функция предоставляет информацию о кодах валют(информация для разработчиков)"

                    "/rub Функция предоставляет актуальную информацию о цене 100 рублей России по отношению к белорусскому рублю"

                    "/usd Функция предоставляет актуальную информацию о цене 1 доллара США по отношению к белорусскому рублю "

                    "/euro Функция предоставляет актуальную информацию о цене 1 Евро по отношению к белорусскому рублю"

                    "/gold Функция предоставляет актуальную информацию о цене 1 грамма золота в белорусских рублях"

                    "/silver Функция предоставляет актуальную информацию о цене 1 грамма серебра в белорусских рублях"

                    "/platinum Функция предоставляет актуальную информацию о цене 1 грамма платины в белорусских рублях"

                    "/palladium Функция предоставляет актуальную информацию о цене 1 грамма палладия в белорусских рублях"

                    "/catalog Функция предоставляет ссылку на сайт, на котором представлена информация о наличии памятных монет"

                    "/metal_period_analytic Функция предоставляет информацию о цене 1 грамма драгоценного металла по выбору за период"

                    "/convert Функция предоставляет возможность перевода суммы из белорусских рублях в иностранную валюту "

                    "/convert1 Функция предоставляет возможность перевода суммы из иностранной валюты в белорусские рубли "

Запуск телеграмм бота с помощью docker:

docker pull avasilevskij/bank:latest

docker run avasilevskij/bank -d


Для запуска телеграмм бота на удалённом сервере с помощью ansible вам нужно выполнить следующую инструкцию:


ВНИМАНИЕ!!! для запуска желательно использовать сервер с Ubuntu


1) Для начала работы нам нужно настроить файлы hosts.txt и ansible.cfg

Про настройку hosts.txt вы можете посмотреть здесь:

https://www.youtube.com/watch?v=O5R6EBdaZZg&list=PLg5SS_4L6LYufspdPupdynbMQTBnZd31N&index=4

А для настройки ansible.cfg откройте его nano ansible.cfg и вставьте следующий текст:

[defaults]
host_key_checking=false
inventory=./hosts.txt

Теперь проверьте подключение серверов с помощью команды:

ansible all -m ping

Должно получиться примерно так:
  









2) Для начала вы должны установить docker на удалённый сервер

Для этого нужно создать playbook_install_docker.yml команда:

nano playbook_install_docker.yml

в открывшеюся файл нужно вставить следующий код:

---
- hosts: #Здесь нужно прописать сервера на которые нужно установить docker
  remote_user: ubuntu
  become: true
  tasks:
    - name: install dependencies
      apt:
        name: "{{item}}"
        state: present
        update_cache: yes
      loop:
        - apt-transport-https
        - ca-certificates
        - curl
        - gnupg-agent
        - software-properties-common
    - name: add GPG key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present
    - name: add docker repository to apt
      apt_repository:
        repo: deb https://download.docker.com/linux/ubuntu bionic stable
        state: present
    - name: install docker
      apt:
        name: "{{item}}"
        state: latest
        update_cache: yes
      loop:
        - docker-ce
        - docker-ce-cli
        - containerd.io
    - name: check docker is active
      service:
        name: docker
        state: started
        enabled: yes
    - name: Ensure group "docker" exists
      ansible.builtin.group:
        name: docker
        state: present
    - name: adding ubuntu to docker group
      user:
        name: ubuntu
        groups: docker
        append: yes
    - name: Install docker-compose
      get_url:
        url: https://github.com/docker/compose/releases/download/1.29.2/docker-compose-Linux-x86_64
        dest: /usr/local/bin/docker-compose
        mode: 'u+x,g+x'
    - name: Change file ownership, group and permissions
      ansible.builtin.file:
        path: /usr/local/bin/docker-compose
        owner: ubuntu
        group: ubuntu 

для запуска playbook нужно ввести команду:

ansible-playbook playbook_install_docker.yml

Про другие варианты установки docker можно прочитать на следующих сайтах: 

https://habr.com/ru/companies/otus/articles/721166/

https://artem.services/?p=1397












3) Затем вы должны установить образ python 3.12 на удалённый сервер:

Для этого нужно создать playbook_install_python.yml команда:

nano playbook_install_python.yml

в открывшеюся папку нужно вставить следующий код:

---
- become: true
  hosts:  #Здесь нужно прописать сервера на которые нужно установить python
  tasks:
      - name: Pull Python Image
        docker_image:
          name: python
          source: pull

для запуска playbook нужно ввести команду:

ansible-playbook playbook_install_python.yml

Документацию по написанию playbook для работы с docker образом можно прочитать на следующем сайте: 

https://docs.ansible.com/ansible/latest/collections/community/docker/docker_container_module.html



4) И теперь вы должны установить образ телеграмм бота на удалённый сервер:

Для этого нужно создать playbook_install_bank.yml команда:

nano playbook_install_bank.yml

в открывшеюся папку нужно вставить следующий код:

---
- become: true
  hosts:  #Здесь нужно прописать сервера на которые нужно установить avasilevskij/bank

  tasks:

      - name: Pull Docker Image
        docker_image:
          name: avasilevskij/bank
          source: pull
          tag: latest

      - name: Start Docker container
        docker_container:
          name: avasilevskij_bank_container
          image: avasilevskij/bank:latest
          state: started

для запуска playbook нужно ввести команду:

ansible-playbook playbook_install_bank.yml

Документацию по написанию playbook для работы с docker образом можно прочитать на следующем сайте: 

https://docs.ansible.com/ansible/latest/collections/community/docker/docker_container_module.html
