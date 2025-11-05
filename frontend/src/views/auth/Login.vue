<template>
    <h1>Login page</h1>

    <form @submit.prevent="login">
        <label for="email">Email</label>
        <input v-model="email" type="email" required>
        <br>
        <label for="password">Password</label>
        <input v-model="password" type="password" required>
        <br><br>
        <button type="submit">Login to account</button>
    </form>
    <p style="color: red;" v-html="message"></p>

</template>
<script>
export default {
    data() {
        return {
            email: '',
            password: '',
            message: ''
        }
    },
    methods: {
        login() {

            fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                }),
            })
                .then(async (response) => {
                    console.log('Response status:', response.status)
                    const data = await response.json()

                    if (response.status === 200) {
                        // ✅ success
                        this.message = `${data.message}. Redirecting to dashboard...`
                        localStorage.setItem('token', data.token)

                        setTimeout(() => {
                            if (data.user.role === 'admin') {
                                this.$router.push('/admin/dashboard')
                            } else {
                                this.$router.push('/user/dashboard')
                            }
                        }, 3000) // 3000 milliseconds = 3 seconds

                    } else if (response.status === 400) {
                        // ⚠️ missing input
                        this.message = 'Please fill in both email and password.'
                    } else if (response.status === 401) {
                        // ❌ already exists
                        this.message = 'Wrong credentials! Please try again'
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