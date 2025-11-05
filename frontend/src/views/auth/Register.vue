<template>
    <h1>Register page</h1>

    <form @submit.prevent="register">
        <label for="name">Name</label>
        <input v-model="name" type="text" required>
        <br>
        <label for="email">Email</label>
        <input v-model="email" type="email" required>
        <br>
        <label for="password">Password</label>
        <input v-model="password" type="password" required>
        <br>
        <label for="password0">Re-Enter Password</label>
        <input v-model="password0" type="password" required>
        <br><br>
        <button type="submit">Create account</button>
    </form>
    <p style="color: red;" v-html="message"></p>

</template>
<script>
export default {
    data() {
        return {
            name: 'user',
            email: 'user@gmil.com',
            password: '1234',
            password0: '1234',
            message: ''
        }
    },
    methods: {
        register() {
            if (this.password != this.password0) {
                this.message = "Retype correct password!"
                return
            }


            fetch('http://127.0.0.1:5000/register', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: this.name,
                    email: this.email,
                    password: this.password,
                }),
            })
                .then(async (response) => {
                    console.log('Response status:', response.status)
                    const data = await response.json()

                    if (response.status === 201) {
                        // ✅ success
                        this.message = `${data.message} <a href="/login">Click here to login</a>.`
                    } else if (response.status === 400) {
                        // ⚠️ missing input
                        this.message = 'Please fill in both email and password.'
                    } else if (response.status === 409) {
                        // ❌ already exists
                        this.message = 'User already exists! Try logging in.'
                    } else {
                        // 🧯 unexpected error
                        this.status = false
                        this.message = 'Something went wrong. Please try again.'
                    }
                })
                .catch((error) => {
                    console.error('Error:', error)
                    this.message = 'Network error. Please try again later.'
                })
        }

    },
    mounted() {
        console.log('Application mounted');
    },
}
</script>