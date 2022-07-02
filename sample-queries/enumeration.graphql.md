query {
  signup(email: "$email|str$", password:"$password|str$") {
    user {
      email
    }
  }
}