db.createCollection('users', { capped: false });
db.users.insert([
    { role: 'MINUTEMAN', username:"admin", password: process.env.ADMIN_PASSWORD}
]);