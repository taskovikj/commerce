# Django and Vue Auction Platform


### 2. Installation

```bash
git clone https://github.com/taskovikj/commerce.git
```



### 2. Build Frontend

```bash
cd vue_frontend
```
```bash
python npm run build
```

### 3.Set up database (On separate terminal)
```bash
cd commerce
```

```bash
python manage.py makemigrations aucions
```
```bash
python manage.py migrate
```


### 4.Build & Launch

```
python manage.py runserver
```

### Documentaion
## Platform Overview

This project is a **listings platform** where users can browse, filter, and interact with various listings. The platform allows users to search listings by name, filter by category, and specify a price range. It also provides features like sorting by the latest or most popular listings and adding/removing items from a personal watchlist.

The platform consists of a **Vue.js** frontend and a **Django** backend.

### Core Features
- **Search and Filtering**: Users can search listings by name, filter by category, and set a price range using input fields and sliders.
- **Watchlist Management**: Users can add or remove listings from their personal watchlist.
- **Sorting**: Listings can be sorted by the latest additions or by the most bids.
- **Pagination**: Listings are paginated, allowing users to navigate between multiple pages of listings.
- **Responsive Design**: The platform is fully responsive, providing an optimal viewing experience across various devices.

### Technologies Used

#### Frontend (Vue.js)
- **Vue.js**
- **Axios**
- **Vue Router**
- **Bootstrap**
- 
#### Backend (Django)
- **Django**
- **MySql Databse**

