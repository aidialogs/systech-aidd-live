# DevOps шаблон для множественных серверов

## Цель

Создать облачные серверы в любом количестве с автоматической настройкой:
- ✅ Доступ по SSH ключу (один ключ на все серверы)
- ✅ Готовность к Docker Compose развертыванию
- ✅ Базовая безопасность (firewall, SSH hardening, fail2ban)
- ✅ Полная автоматизация (одна команда на весь деплой)

## КЛЮЧЕВЫЕ ТРЕБОВАНИЯ

### 1. Множественные серверы
- Параметр `server_count` в Terraform 
- Все серверы создаются абсолютно идентичными

### 2. Единый SSH ключ
- **Один** ключ на все серверы
- Автогенерация ED25519 ключа через TLS provider

### 3. Только базовая настройка
- ✅ **Включено:** Docker CE + Compose V2, firewall (iptables), SSH hardening, fail2ban, системный пользователь
- Ansible роли: `common`, `docker`, `security`

### 4. Облачный провайдер
- **Timeweb Cloud** (российский провайдер с Terraform support)
- Документация: https://github.com/timeweb-cloud/terraform-provider-timeweb-cloud
- Provider: `tf.timeweb.cloud/timeweb-cloud/timeweb-cloud` версия `~> 1.0`
- OS: Ubuntu 22.04 LTS (data source: `twc_os`)
- Конфигуратор через location (data source: `twc_configurator`)

### 5. Качество и простота
- Понятный, простой и поддерживаемый код
- Минимальные зависимости (только встроенные Ansible модули)
- Makefile со всеми основными операциями
- Bash скрипт для полной автоматизации

## Архитектурные принципы

### Terraform: Infrastructure as Code

**Ключевые концепции:**

1. **Модульность через count**
   - Использовать `resource "twc_server" "servers" { count = var.server_count }`
   - Создавать IPv4 адреса отдельным ресурсом с count
   - Генерация inventory через templatefile с циклом по серверам

2. **SSH ключи**
   - TLS provider для генерации ED25519 (более безопасен чем RSA)
   - Условное создание: генерация ИЛИ использование существующего
   - Upload в Timeweb через `twc_ssh_key` ресурс
   - Сохранение локально через `local_file` с правильными правами (0600 для private)

3. **Автогенерация Ansible inventory**
   - Template file с циклом: `for i in range(var.server_count)`
   - Абсолютные пути к SSH ключам через `abspath()`
   - Группы серверов: `[servers]` для всех хостов
   - Variables: `ansible_user=root`, `ansible_python_interpreter=/usr/bin/python3`
   - SSH args: отключение StrictHostKeyChecking для первого подключения

4. **Outputs**
   - Массив IP адресов всех серверов
   - Массив команд SSH для подключения
   - Понятные next steps инструкции с ASCII-art форматированием

**Структура переменных:**
- `twc_token` (sensitive, обязательная)
- `project_name` (default: "systech-username")
- `server_count` (default: 1, validation: 1-10)
- `location` (default: "ru-1")
- `server_config` (object: cpu, ram, disk с разумными дефолтами 2/2048/40960)
- `generate_ssh_key` (bool, default: true)
- `ssh_public_key_path` (используется только если generate_ssh_key = false)

---

### Ansible: Configuration Management

**Ключевые концепции:**

1. **Трехролевая архитектура**
   
   **Роль: common**
   - Обновление системы (apt update + upgrade)
   - Установка базовых пакетов (принцип: только необходимое - curl, git, jq, nano, vim, htop)
   - Создание системного пользователя с именем проекта
   - Копирование SSH ключей от root к app user
   - Создание директорий: `/opt/${project_name}` с подпапками (data, logs, config, backup)
   - Настройка timezone (UTC по умолчанию)

   **Роль: docker**
   - Удаление старых версий Docker (если есть)
   - Добавление official Docker repository через GPG ключ (dearmored формат для современных систем)
   - Установка пакетов: docker-ce, docker-ce-cli, containerd.io, docker-compose-plugin
   - Конфигурация daemon.json (log rotation: max-size 50m, max-file 3)
   - Добавление app user в docker группу
   - ВАЖНО: НЕ перезагружать сессию - новая группа применится при следующем логине
   - Проверка установки: `docker --version` и `docker compose version`

   **Роль: security**
   - **Firewall:** iptables через iptables-persistent
     - Принцип: default DROP для INPUT, ACCEPT для OUTPUT
     - Разрешить: loopback, established/related, порты 22/80/443/8000
     - Сохранение в `/etc/iptables/rules.v4`
   - **SSH hardening:** Правка sshd_config БЕЗ перезагрузки (опасно!)
     - PermitRootLogin prohibit-password (ключи работают)
     - PasswordAuthentication no
     - PubkeyAuthentication yes
     - MaxAuthTries 3
   - **Fail2ban:** защита SSH от bruteforce
     - jail.local: maxretry=3, bantime=3600
     - Только SSH jail, остальное не нужно

2. **Принципы реализации ролей**

   - **Идемпотентность:** все задачи должны быть безопасны для повторного запуска
   - **Использование только builtin модулей:** НЕ использовать community.general (упрощение зависимостей)
   - **Defaults в roles/*/defaults/main.yml:** все настраиваемые параметры вынести в defaults
   - **Handlers:** минимальные (только restart docker, restart fail2ban)
   - **Проверки:** assert для системных требований (Ubuntu 20.04+, RAM 1GB+)
   - **Информативность:** debug сообщения с emoji для важных этапов

3. **Playbook структура**

   - Один playbook: `base-setup/playbooks/setup.yml`
   - Target hosts: `servers` (из inventory)
   - `become: yes` для всего playbook
   - Pre-tasks: информация о деплое, проверка требований, wait_for_connection
   - Роли в порядке: common → docker → security
   - Post-tasks: проверка Docker от имени app user, summary с инструкциями

4. **Ansible.cfg настройки**

   ```ini
   inventory = inventory.ini
   host_key_checking = False
   timeout = 30
   forks = 10  # Параллельность для множественных серверов
   stdout_callback = yaml  # Красивый вывод
   ```

---

## АВТОМАТИЗАЦИЯ

### Makefile

**Принцип:** Удобные shortcuts для всех операций, не требующие знания Terraform/Ansible

**Обязательные команды:**
- `help` - показать все команды (default target)
- `setup` - копирование terraform.tfvars.example → terraform.tfvars
- `init` - terraform init
- `apply` - создание инфраструктуры
- `setup-servers` - запуск Ansible base-setup
- `deploy` - полная автоматизация (вызов deploy.sh)
- `status` - показать состояние серверов (IP, uptime)
- `output` - terraform output
- `test-connection` - ansible ping
- `destroy` - удаление инфраструктуры (с подтверждением!)
- `clean` - очистка временных файлов

**Стилистика:**
- Цветной вывод (BLUE, GREEN, YELLOW, RED)
- Защита от случайного destroy (интерактивное подтверждение)
- Извлечение project_name из group_vars автоматически

### Deploy Script (deploy.sh)

**Цель:** Полностью автоматический деплой от 0 до готовых серверов одной командой

**Фазы:**
1. **Проверка требований** - terraform, ansible установлены
2. **Проверка конфигурации** - terraform.tfvars существует
3. **Terraform apply** - создание инфраструктуры
4. **Ожидание** - 60 секунд для инициализации серверов
5. **Ansible ping** - проверка SSH доступности (retry если не работает)
6. **Ansible playbook** - выполнение base-setup
7. **Verification** - проверка Docker на всех серверах
8. **Summary** - вывод IP, SSH команд, next steps

**Принципы:**
- `set -euo pipefail` для строгости
- Цветной вывод с emoji
- Информативные сообщения на каждом шаге
- Graceful handling ошибок (не падать сразу, показать что проверить)

---

## Критические детали реализации

### Terraform

1. **Inventory template** должен использовать цикл:
   ```
   %{~ for server in servers ~}
   ${server.name} ansible_host=${server.ip} ...
   %{~ endfor ~}
   ```

2. **SSH key permissions:** private key должен быть 0600 (file_permission в local_file)

3. **Dependencies:** local_file.ansible_inventory должен иметь `depends_on = [twc_server_ip.server_ipv4]`

4. **Абсолютные пути:** использовать `abspath()` для путей к ключам в inventory

### Ansible

1. **Docker GPG key:** ОБЯЗАТЕЛЬНО использовать dearmored формат (`gpg --dearmor`)
   - Старый формат (без --dearmor) не работает на современных Ubuntu

2. **Docker packages:** точный список:
   - docker-ce
   - docker-ce-cli  
   - containerd.io
   - docker-buildx-plugin
   - docker-compose-plugin (НЕ отдельный docker-compose!)

3. **SSH hardening БЕЗ перезагрузки:**
   - НЕ добавлять notify для reload ssh в security роли
   - Добавить debug warning что SSH не перезагружен (это безопасно)
   - Пользователь перезагрузит вручную после проверки

4. **Firewall через shell модуль:**
   - Ansible builtin iptables модуль сложный и багованный
   - Лучше использовать shell с полным скриптом
   - Template для портов: `{% for port in firewall_allowed_ports %}`

5. **App user SSH keys:**
   - Копировать от root используя `remote_src: yes`
   - Проверять существование через stat перед копированием

### Deploy Script

1. **Wait times:**
   - После terraform apply: 60 секунд минимум
   - Если ansible ping fail: +30 секунд retry

2. **Error handling:**
   - Проверять существование terraform.tfvars перед запуском
   - Graceful fail если ansible не может подключиться (показать команду для ручной проверки)

3. **Verification:**
   - Тестировать SSH как app user (не root)
   - Тестировать docker --version от app user
