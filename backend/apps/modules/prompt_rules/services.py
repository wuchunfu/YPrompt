from sanic.log import logger

class PromptRulesService:
    """用户提示词规则服务"""
    
    def __init__(self, db):
        self.db = db
    
    async def get_user_rules(self, user_id: int):
        """获取用户的提示词规则"""
        try:
            sql = "SELECT * FROM user_prompt_rules WHERE user_id = ?"
            rules = await self.db.get(sql, [user_id])
            return rules
        except Exception as e:
            logger.error(f'❌ 获取用户提示词规则失败: {e}')
            raise
    
    async def save_user_rules(self, user_id: int, rules_data: dict):
        """保存或更新用户的提示词规则"""
        try:
            # 检查用户规则是否存在
            existing = await self.get_user_rules(user_id)
            
            if existing:
                # 更新现有规则
                sql = """
                UPDATE user_prompt_rules 
                SET system_prompt_rules = ?,
                    user_guided_prompt_rules = ?,
                    requirement_report_rules = ?,
                    thinking_points_extraction_prompt = ?,
                    thinking_points_system_message = ?,
                    system_prompt_generation_prompt = ?,
                    system_prompt_system_message = ?,
                    optimization_advice_prompt = ?,
                    optimization_advice_system_message = ?,
                    optimization_application_prompt = ?,
                    optimization_application_system_message = ?,
                    quality_analysis_system_prompt = ?,
                    user_prompt_quality_analysis = ?,
                    user_prompt_quick_optimization = ?,
                    user_prompt_rules = ?
                WHERE user_id = ?
                """
                await self.db.execute(sql, [
                    rules_data.get('system_prompt_rules'),
                    rules_data.get('user_guided_prompt_rules'),
                    rules_data.get('requirement_report_rules'),
                    rules_data.get('thinking_points_extraction_prompt'),
                    rules_data.get('thinking_points_system_message'),
                    rules_data.get('system_prompt_generation_prompt'),
                    rules_data.get('system_prompt_system_message'),
                    rules_data.get('optimization_advice_prompt'),
                    rules_data.get('optimization_advice_system_message'),
                    rules_data.get('optimization_application_prompt'),
                    rules_data.get('optimization_application_system_message'),
                    rules_data.get('quality_analysis_system_prompt'),
                    rules_data.get('user_prompt_quality_analysis'),
                    rules_data.get('user_prompt_quick_optimization'),
                    rules_data.get('user_prompt_rules'),
                    user_id
                ])
                logger.info(f'✅ 更新用户提示词规则成功: user_id={user_id}')
            else:
                # 创建新规则
                rules_data['user_id'] = user_id
                await self.db.table_insert('user_prompt_rules', rules_data)
                logger.info(f'✅ 创建用户提示词规则成功: user_id={user_id}')
            
            # 返回更新后的规则
            return await self.get_user_rules(user_id)
            
        except Exception as e:
            logger.error(f'❌ 保存用户提示词规则失败: {e}')
            raise
    
    async def delete_user_rules(self, user_id: int):
        """删除用户的提示词规则（重置为默认）"""
        try:
            sql = "DELETE FROM user_prompt_rules WHERE user_id = ?"
            await self.db.execute(sql, [user_id])
            logger.info(f'✅ 删除用户提示词规则成功: user_id={user_id}')
        except Exception as e:
            logger.error(f'❌ 删除用户提示词规则失败: {e}')
            raise
