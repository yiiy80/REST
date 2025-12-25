const userModel = require('../models/userModel');

// 获取所有用户
exports.getAllUsers = (req, res) => {
  const users = userModel.getAllUsers();
  res.status(200).json(users);
};

// 获取单个用户
exports.getUserById = (req, res) => {
  const user = userModel.getUserById(req.params.id);
  if (user) {
    res.status(200).json(user);
  } else {
    res.status(404).json({ message: '用户不存在' });
  }
};

// 创建用户
exports.createUser = (req, res) => {
  const { name, email, password } = req.body;
  
  // 简单验证
  if (!name || !email || !password) {
    return res.status(400).json({ message: '请提供完整的用户信息' });
  }
  
  const newUser = userModel.createUser({ name, email, password });
  res.status(201).json(newUser);
};

// 更新用户
exports.updateUser = (req, res) => {
  const updatedUser = userModel.updateUser(req.params.id, req.body);
  if (updatedUser) {
    res.status(200).json(updatedUser);
  } else {
    res.status(404).json({ message: '用户不存在' });
  }
};

// 删除用户
exports.deleteUser = (req, res) => {
  const deletedUser = userModel.deleteUser(req.params.id);
  if (deletedUser) {
    res.status(200).json({ message: '用户已删除', user: deletedUser });
  } else {
    res.status(404).json({ message: '用户不存在' });
  }
};