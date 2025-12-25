// 用户数据存储（内存方式）
let users = [];
let nextId = 1;

// 用户模型
class User {
  constructor(name, email, password) {
    this.id = nextId++;
    this.name = name;
    this.email = email;
    this.password = password; // 实际项目中应该加密存储
    this.createdAt = new Date().toISOString();
    this.updatedAt = new Date().toISOString();
  }
}

// 获取所有用户
exports.getAllUsers = () => {
  return users;
};

// 根据ID获取用户
exports.getUserById = (id) => {
  return users.find(user => user.id === parseInt(id));
};

// 创建新用户
exports.createUser = (userData) => {
  const newUser = new User(userData.name, userData.email, userData.password);
  users.push(newUser);
  return newUser;
};

// 更新用户
exports.updateUser = (id, userData) => {
  const index = users.findIndex(user => user.id === parseInt(id));
  if (index !== -1) {
    users[index] = {
      ...users[index],
      ...userData,
      id: parseInt(id), // 确保ID不变
      updatedAt: new Date().toISOString()
    };
    return users[index];
  }
  return null;
};

// 删除用户
exports.deleteUser = (id) => {
  const index = users.findIndex(user => user.id === parseInt(id));
  if (index !== -1) {
    const deletedUser = users[index];
    users.splice(index, 1);
    return deletedUser;
  }
  return null;
};