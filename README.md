<a id="readme-top"></a>

<div align="center">
  <h1 align="center">Todo; A Django Web App</h1>


  <img src="https://github.com/BlackBaron94/Todo-Django-App/actions/workflows/tests.yml/badge.svg" alt="Tests"/>
  <a href="https://codecov.io/gh/BlackBaron94/Todo-Django-App" > 
  <img src="https://codecov.io/gh/BlackBaron94/Todo-Django-App/graph/badge.svg?token=QXBRFLQ1JI"/> 
  </a>


  <p align="center">
    Fullstack web project δημιουργημένο με Django που υποστηρίζει τη δημιουργία, ανάγνωση, επεξεργασία και διαγραφή αντικειμένων μιας Todo list για τον logged in χρήστη!
  </p>
  <p align="center">
    Δείτε την <a href="https://todo-django-app-miwk.onrender.com">εδώ</a>.
  </p>
</div>

## Περιεχόμενα
- [Περιγραφή Project](#περιγραφή-project)
- [CI/CD και Testing](#cicd-και-testing)
- [Οδηγίες Εγκατάστασης](#οδηγίες-εγκατάστασης)
- [Χρήση](#χρήση)
- [Μελλοντικές Προσθήκες](#μελλοντικές-προσθήκες)
- [Επικοινωνία](#επικοινωνία)
- [License](#license)

## Περιγραφή Project 

Η εφαρμογή δημιουργήθηκε με σκοπό τη δημιουργία ενός απλού Todo list για τον κάθε χρήστη. Ο χρήστης, μετά το signup & login, έχει τις παρακάτω δυνατότητες:
* Να δημιουργήσει νέα tasks.
* Να δει όλα τα δικά του tasks.
* Να επεξεργαστεί την περιγραφή του κάθε task.
* Να τσεκάρει τα tasks που έχουν ολοκληρωθεί.
* Να διαγράψει tasks του.

Η εφαρμογή έχει ανεβεί στο Render και επικοινωνεί με βάση δεδομένων PostgreSQL που είναι ανεβασμένη επίσης στο Render.

*Σημείωση: Οι έλεγχοι του κωδικού (όπως η απαίτηση να μην είναι αριθμητικός ή πολύ απλός) υλοποιούνται από το σύστημα αυθεντικοποίησης του Django και δεν τροποποιήθηκαν.*

### Τεχνολογίες και βιβλιοθήκες που χρησιμοποιήθηκαν

<a href="https://python.org/"> <img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&style=plastic" alt="Python-logo" width=120px/></a>

<a href="https://www.djangoproject.com/"> <img src="https://img.shields.io/badge/-Django-092E20?style=flat&logo=Django&style=plastic" alt="Django-logo" width=120px/></a>

<a href="https://www.postgresql.org/"> <img src="https://img.shields.io/badge/-PostgreSQL-yellow?style=flat&logo=postgresql&style=plastic" alt="PostgreSQL-logo" width=140px height=32px/></a>

<a href="https://gunicorn.org/"> <img src="https://img.shields.io/badge/-Gunicorn-blue?style=flat&logo=gunicorn&style=plastic" alt="Gunicorn-logo" width=140px height=32px/></a>

<a href="https://www.w3schools.com/html/"> <img src="https://img.shields.io/badge/%20-HTML-blue?logo=HTML5&logoColor=white-HTML&style=plastic" alt="HTML-Logo" width=100px/></a>

<a href="https://www.w3schools.com/css/"> <img src="https://img.shields.io/badge/%20-CSS-663399?logo=CSS&logoColor=white-CSS&style=plastic" alt="CSS-Logo" width=90px/></a>

<a href="https://github.com/features/actions"> <img src="https://img.shields.io/badge/%20-GitHubActions-0A1F44?logo=githubactions&logoColor=2088FF-GitHubActions&style=plastic" alt="GitHubActions-Logo" width=223px height=39px/></a>

### Δομή του Project

```bash
.
├── .github/workflows/  # GitHub Actions για CI
├── mysite/             # Ρυθμίσεις Django project (settings, urls, wsgi)
├── static/             # Στατικά αρχεία CSS
├── todo/               # Η κύρια εφαρμογή (models, views, urls, tests, templates)
│   ├── migrations/
│   ├── templates/
│   │   ├── registration/    # Templates για signup, login, logged_out
│   │   ├── todo/            # Templates για όλες τις υπόλοιπες σελίδες της εφαρμογής (index, create, edit ...)
├── .env.example        # Αρχείο παράδειγμα για τις ρυθμίσεις των environment variables που απαιτούνται
├── .gitignore
├── LICENSE
├── manage.py
└── requirements.txt
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## CI/CD και Testing

Το project χρησιμοποιεί [GitHub Actions](https://github.com/features/actions) για την αυτοματοποιημένη εκτέλεση δοκιμών (tests) σε κάθε αλλαγή στον κώδικα (push ή pull request στο main branch).

Ορίζεται στο αρχείο `.github/workflows/tests.yml` και περιλαμβάνει αυτόματη εγκατάσταση dependencies και εκτέλεση των tests.

Το badge στο πάνω μέρος δείχνει την τρέχουσα κατάσταση των tests και το ποσοστό του κώδικα που καλύπτεται από αυτά.

Η εφαρμογή καλύπτεται με **25+ tests**, οργανωμένα με χρήση του Django `TestCase`. Παρέχουν κάλυψη περί το 94% και περιλαμβάνουν:
- Model logic:
  
  ✔ Έλεγχος string representation
  
  ✔ Προεπιλεγμένη κατάσταση `completed=False`
  
- CRUD logic των tasks:
  
  ✔ Προσθήκη, επεξεργασία, διαγραφή
  
  ✔ Ενημέρωση κατάστασης (completed/pending)
  
  ✔ Έλεγχος ορίων (μήκος περιγραφής task)
  
- Authorization/Authentication:
  
  ✔ Χρήστες δεν μπορούν να δουν ή να αλλάξουν tasks άλλων χρηστών
  
  ✔ Redirects όταν δεν έχει γίνει login (@login_required)
  
  ✔ Redirects σε `/todo/` αν ο χρήστης είναι logged in και προσπαθεί να πάει στη url `/login/ ` ή στη `/signup/`
  
- HTTP method control & form validation:
  
  ✔ Απαγόρευση GET σε views που απαιτούν POST (@require_POST)
  
  ✔ Έλεγχος για άδεια ή non valid submissions
  
- General Redirection behavior:
  
  ✔ Επιστροφή στο `/todo/` μετά από κάθε ενέργεια
  
  ✔ Προστασία από unauthorized access με redirects σε `/login/`

Τα tests εκτελούνται αυτόματα με κάθε αλλαγή στο repository μέσω [GitHub Actions](https://github.com/features/actions) και τα αποτελέσματα καταγράφονται
στο [Codecov](https://about.codecov.io/).

> Δείτε το αρχείο [tests.py](./todo/tests.py).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Οδηγίες Εγκατάστασης

### Για να τρέξει το project τοπικά:


1. Clone του repo
   ```sh
   git clone https://github.com/BlackBaron94/Todo-Django-App.git
   cd Todo-Django-App
   ```


2. Δημιουργία και ενεργοποίηση virtual environment
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   ή
   venv\Scripts\activate     # Windows
   ```
   
3. Εγκατάσταση απαιτουμένων
   ```sh
   pip install -r requirements.txt
   ```

4. Ρύθμιση των environment variables σε αρχείο .env όπως φαίνεται στο .env.example. (απαιτείται εγκατεστημένη PostgreSQL)
- PostgreSQL:
   ```sh
   DB_NAME=todo_db
   DB_USER=postgres
   DB_PASSWORD=your_db_password_here
   DB_HOST=localhost
   DB_PORT=5432

   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```
   
- Για να τρέξει τοπικά με SQLite3 εισάγετε τον παρακάτω κώδικα στο settings.py:
  ```python
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
  }
  ```

5. Εκτέλεση migrate και δημιουργία superuser (απαιτεί εισαγωγή username + email + password)
   ```sh
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Εκκίνηση του server:
   ```sh
   python manage.py runserver
   ```

7. Πλοήγηση με browser στη διεύθυνση <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a>.

   
<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Χρήση


1. Signup - Ο χρήστης μπορεί να δημιουργήσει νέο λογαριασμό μέσω της φόρμας εγγραφής. Χρησιμοποιείται το UserCreationForm της Django, το οποίο ενσωματώνει έτοιμη λογική ασφαλείας για τη δημιουργία χρηστών, καθώς και ελέγχους ισχυρότητας κωδικού.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Todo-Django-App/Signup.jpg" alt="Signup" width="750"/>
</div>

----

2. Login - Ο χρήστης μπορεί να εισέλθει στο λογαριασμό του και να δει τις βασικές σελίδες της εφαρμογής.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Todo-Django-App/Login.jpg" alt="Login" width="750"/>
</div>

----

3. Home Page - Ο χρήστης βλέπει όλα τα tasks του και μπορεί να αλληλεπιδράσει με αυτά (προσθήκη, επεξεργασία, διαγραφή, μαρκάρισμα ως ολοκληρωμένα).

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Todo-Django-App/Home_page.jpg" alt="Home_page" width="750"/>
</div>

----

4. Add Task - Ο χρήστης εδώ μπορεί να συμπληρώσει την περιγραφή του task και να το προσθέσει στο Todo list του και ειδοποιείται με το ανάλογο μήνυμα.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Todo-Django-App/Add_task.jpg" alt="Add_task" width="750"/>
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Todo-Django-App/Task_added.jpg" alt="Task_added" width="750"/>
</div>

----

5. Check Task - Όταν ο χρήστης τσεκάρει ένα task ενημερώνεται με το κατάλληλο μήνυμα και βλέπει οπτικά την αλλαγή με το task crossed out.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Todo-Django-App/Task_completed.jpg" alt="Task_completed" width="750"/>
</div>

----

6. Edit Task - Ο χρήστης πατώντας στο μολύβι δίπλα από κάποιο task, μπορεί να το επεξεργαστεί στην παρακάτω οθόνη.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Todo-Django-App/Edit_task.jpg" alt="Edit_task" width="750"/>
</div>

----

7. Delete Task - Πατώντας στο Χ δίπλα από κάποιο task ο χρήστης μπορεί να διαγράψει το συγκεκριμένο task επιβεβαιώνοντας τη διαγραφή στην παρακάτω οθόνη.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Todo-Django-App/Task_deletion.jpg" alt="Task_deletion" width="750"/>
</div>


<i> **Σημείωση:**  
 Το Render μπορεί να χρειαστεί 30–50 δευτερόλεπτα για να ξεκινήσει το deploy της ιστοσελίδας.
 Αν δείτε "APPLICATION LOADING...", παρακαλώ περιμένετε.</i>


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Μελλοντικές Προσθήκες

- [X] Προσθήκη authentication.
- [X] Διαχείριση task με περιγραφή μεγαλύτερη των 200 χαρακτήρων (όριο task_text field στο DB).
- [X] Προσθήκη CI/CD pipeline με tests για edge cases.
- [ ] Φίλτρο tasks (ημερομηνία, κατάσταση).
- [ ] Ταξινόμηση tasks (ημερομηνία, κατάσταση).
- [ ] Προσθήκη deadlines για tasks και νέας κατάστασης task (failed to meet deadline).
- [ ] Προσθήκη tests για POST edit/delete tasks άλλων users.
- [ ] Προσθήκη tests για 405 method not allowed σε GET/POST.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Επικοινωνία

Γιώργος Τσολακίδης - [Linked In: Giorgos Tsolakidis](https://www.linkedin.com/in/black-baron/) - black_baron94@hotmail.com 

Project Link: [Todo Django App](https://github.com/BlackBaron94/Todo-Django-App)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## License


This project is licensed under the MIT License – see the [LICENSE](./LICENSE) file for details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

