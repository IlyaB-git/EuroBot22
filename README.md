# EuroBot22


Получение изменений из удалённого репозитория
-------------------------------------


Для загрузки изменений из удалённого репозитория используется параметр pull. Он скачивает копию текущей ветки с указанного удалённого репозитория и объединяет её с локальной копией.


git pull
--------------

Также можно просмотреть подробные сведения о загруженных файлах с помощью флага --verbose.

git pull --verbose


Отправка изменений в удалённый репозиторий
-----------------------------
Отправлять изменения в удалённый репозиторий можно параметром push с указанием имени репозитория и ветки.

git push EuroBot22 main
--------------------


Эта команда передаёт локальные изменения в центральный репозиторий, где с ними могут ознакомиться другие участники проекта.



Слияние двух веток
------------------
Объединить две ветки можно параметром merge с указанием имени ветки. Команда объединит указанную ветку с основной.

git merge existing_branch_name

Если надо выполнить коммит слияния, выполните команду git merge с флагом --no-ff.

git merge --no-ff existing_branch_name

Указанная команда объединит заданную ветку с основной и произведёт коммит слияния. Это необходимо для фиксации всех слияний в вашем репозитории.

Создание новой ветки и переход в неё
-----------------------------------

Создать новую ветку можно с помощью параметра branch, указав имя ветки.

git branch new_branch_name

Но Git не переключится на неё автоматически. Для автоматического перехода нужно добавить флаг -b и параметр checkout.

git checkout -b new_branch_name

При создании коммита в репозитории можно добавить однострочное сообщение с помощью параметра commit с флагом -m. Само сообщение вводится непосредственно после флага, в кавычках.

git commit -m "Your short summary about the commit"
----------------------------------

Просматривать изменения, внесённые в репозиторий, можно с помощью параметра log. Он отображает список последних коммитов в порядке выполнения. Кроме того, добавив флаг -p, вы можете подробно изучить изменения, внесённые в каждый файл.

git log -p
------------

Откатить последний коммит можно с помощью параметра revert. Создастся новый коммит, содержащий обратные преобразования относительно предыдущего, и добавится к истории текущей ветки.

git revert HEAD
-------------
