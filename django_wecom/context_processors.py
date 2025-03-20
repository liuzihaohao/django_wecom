def get_var(request):
    """
    识别 user_agent 是否包含 wxwork 字样，并覆给 is_in_wecom 传入模板
    """

    is_in_wecom = False
    user_agent = request.META.get('HTTP_USER_AGENT')
    if "wxwork" in user_agent:
        is_in_wecom = True
    return {"is_in_wecom": is_in_wecom}