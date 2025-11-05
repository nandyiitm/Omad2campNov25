<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>

    <section class="form-section">
      <h3>Create New Pizza</h3>

      <form @submit.prevent="create_pizza" class="pizza-form">
        <div class="form-group">
          <label for="name">Pizza Name:</label>
          <input
            v-model="name"
            type="text"
            id="name"
            placeholder="Enter pizza name"
            required
          />
        </div>

        <div class="form-group">
          <label>Has Toppings:</label>
          <div class="radio-group">
            <label>
              <input type="radio" value="true" v-model="toppings" required />
              Yes
            </label>
            <label>
              <input type="radio" value="false" v-model="toppings" required />
              No
            </label>
          </div>
        </div>

        <button type="submit" class="btn">Add Pizza</button>
      </form>

      <p v-if="message" :class="status ? 'success' : 'error'" v-html="message"></p>
    </section>

    <section class="pizza-list-section">
      <h3>Pizza List</h3>

      <!-- Loading indicator -->
      <p v-if="loading" class="loading">Loading pizzas...</p>

      <!-- Pizza list -->
      <ol v-else-if="pizzas.length" class="pizza-list">
        <li v-for="pizza in pizzas" :key="pizza.id" class="pizza-item">
          <a :href="'/admin/pizza/' + pizza.id" class="pizza-link">
            {{ pizza.name }} -
            <span class="toppings">{{ pizza.toppings ? 'Yes' : 'No' }}</span>
          </a>
          <button class="btn delete-btn" @click="deletePizza(pizza.id)">Delete</button>
        </li>
      </ol>

      <!-- Empty state -->
      <p v-else class="no-pizzas">No pizzas available. Add one above!</p>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pizzas: [],
      name: '',
      toppings: '',
      message: '',
      status: null,
      loading: false, // ⏳ new state
    }
  },
  methods: {
    async load_pizzas() {
      const token = localStorage.getItem('token')
      this.loading = true
      try {
        const response = await fetch('http://127.0.0.1:5000/items', {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        })
        const data = await response.json()
        if (response.status === 200) {
          this.pizzas = data.items || []
        } else if (response.status === 401 || response.status === 422) {
          alert('Unauthorized access. Please log in.')
          this.$router.push('/login')
        } else {
          this.status = false
          this.message = 'Something went wrong while loading pizzas.'
        }
      } catch (err) {
        console.error(err)
        this.status = false
        this.message = 'Network error. Please try again later.'
      } finally {
        this.loading = false // ✅ stop loading
      }
    },

    async create_pizza() {
      const token = localStorage.getItem('token')
      try {
        const response = await fetch('http://127.0.0.1:5000/items', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            name: this.name,
            color: this.toppings === 'true',
          }),
        })

        const data = await response.json()

        if (response.status === 201) {
          this.status = true
          this.message = `🍕 Pizza "${this.name}" added successfully!`
          this.name = ''
          this.toppings = ''
          this.load_pizzas()
        } else if (response.status === 400) {
          this.status = false
          this.message = 'Please fill in all pizza details.'
        } else if (response.status === 401 || response.status === 422) {
          alert('Unauthorized access. Please log in again.')
          this.$router.push('/login')
        } else {
          this.status = false
          this.message = 'Error adding pizza. Try again later.'
        }
      } catch {
        this.status = false
        this.message = 'Network error. Please try again later.'
      }
    },

    async deletePizza(pizzaId) {
      const token = localStorage.getItem('token')
      try {
        const response = await fetch(`http://127.0.0.1:5000/items/${pizzaId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        })
        const data = await response.json()
        if (response.status === 200) {
          this.status = true
          this.message = 'Pizza deleted successfully!'
          this.load_pizzas()
        } else if (response.status === 401 || response.status === 422) {
          alert(data.message)
          this.$router.push('/login')
        } else {
          this.status = false
          this.message = 'Error deleting pizza. Try again later.'
        }
      } catch {
        this.status = false
        this.message = 'Network error. Please try again later.'
      }
    },
  },
  mounted() {
    this.load_pizzas()
  },
}
</script>


<style scoped>
.admin-dashboard {
  max-width: 700px;
  margin: 60px auto;
  padding: 30px;
  background: #fffaf3;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Poppins', sans-serif;
  color: #333;
}

h1 {
  color: #d35400;
  text-align: center;
  margin-bottom: 30px;
}

h3 {
  color: #e67e22;
  margin-bottom: 10px;
}

.form-section {
  margin-bottom: 40px;
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #f6c667;
}

.pizza-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  text-align: left;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 5px;
  color: #555;
}

.radio-group {
  display: flex;
  gap: 15px;
  margin-top: 5px;
}

input[type='text'] {
  width: 100%;
  padding: 10px;
  border: 1px solid #f0b35f;
  border-radius: 6px;
  font-size: 1rem;
  transition: border 0.3s;
}

input[type='text']:focus {
  outline: none;
  border-color: #e67e22;
}

.btn {
  padding: 10px 16px;
  background: #e67e22;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  font-weight: 600;
}

.btn:hover {
  background: #cf6d17;
  transform: scale(1.05);
}

.delete-btn {
  background: #e74c3c;
  margin-left: 15px;
}

.delete-btn:hover {
  background: #c0392b;
}

.pizza-list {
  list-style: none;
  padding: 0;
}

.pizza-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  padding: 12px 16px;
  border: 1px solid #f7c873;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.pizza-item:hover {
  transform: scale(1.02);
  box-shadow: 0 3px 10px rgba(241, 196, 15, 0.2);
}

.pizza-link {
  text-decoration: none;
  color: #d35400;
  font-weight: 600;
}

.toppings {
  color: #666;
  font-weight: 400;
}

.no-pizzas {
  color: #999;
  text-align: center;
  font-style: italic;
  margin-top: 10px;
}

.success {
  color: #27ae60;
  font-weight: bold;
  margin-top: 10px;
}

.error {
  color: #e74c3c;
  font-weight: bold;
  margin-top: 10px;
}
</style>