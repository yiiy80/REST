const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// 定义所有用户相关路由
router.get('/', userController.getAllUsers);        // 获取所有用户
router.get('/:id', userController.getUserById);     // 获取单个用户
router.post('/', userController.createUser);        // 创建新用户
router.put('/:id', userController.updateUser);      // 更新用户
router.delete('/:id', userController.deleteUser);   // 删除用户

module.exports = router;