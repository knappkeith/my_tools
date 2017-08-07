js_login = '''javascript:(
    function(){{
        var user = '{my_user}';
        var pass = '{my_pass}';
        var url = '{my_url}';
        var user_id = '{my_user_element_id}';
        var pass_id = '{my_pass_element_id}';
        var button_id = '{my_button_element_id}';
        if (window.location.href.includes(url)){{
            document.getElementById(user_id).value = user;
            document.getElementById(pass_id).value = pass;
            document.getElementById(button_id).click();
        }}else{{
            window.location.href = url;
        }}
    }}
)();'''

js_amazon_lamba = '''javascript:(
    function(){{
        var values = {{
            {my_values_dict}
        }};
        var headers = document.getElementsByClassName("header-section")[0].getElementsByTagName("div");
        console.log(headers);
        for (i=0;i<headers.length;i++){{
            console.log(i);
            console.log(headers[i]);
            if (headers[i].className.includes("form-group")) {{
                if (headers[i].textContent.trim() in values) {{
                    headers[i].getElementsByTagName("input")[0].value = "-" + values[headers[i].textContent.trim()];
                }}
            }}
        }}
        var stageVars = document.getElementsByClassName("stage-variables-section")[0].getElementsByTagName("div");
        console.log(stageVars);
        for (i=0;i<stageVars.length;i++) {{
            console.log(i);
            console.log(stageVars[i]);
            if (stageVars[i].className.includes("form-group")) {{
                console.log(stageVars[i].textContent);
                if (stageVars[i].textContent.trim() in values {{
                    console.log("i in");
                    stageVars[i].getElementsByTagName("input")[0].value = "-" + values[stageVars[i].textContent.trim()];
                }}
            }}
        }}
    }}
)();'''

def _build_shortcut(shortcut_string, my_variables, debug):
    if not debug:
        formatted_str = "".join([
            x.strip()
            for x in shortcut_string.split('\n')
            if "console.log(" not in x])
    else:
        formatted_str = "".join([x.strip() for x in shortcut_string.split('\n')])
    return formatted_str.format(**my_variables)

def shortcut_login(
        my_user, my_pass, my_url,
        my_user_element_id="textfield-1024-inputEl",
        my_pass_element_id="textfield-1025-inputEl",
        my_button_element_id="button-1027-btnInnerEl",
        debug=False):
    ce_env = {'PROD': "api", 'SNAPSHOT': "snapshot", 'STAGING': "staging"}
    if my_url.upper() in ce_env.keys():
        my_url = "https://{env}.cloud-elements.com/elements/jsp/login.jsp".format(
            env=ce_env[my_url.upper()])
    my_vars = {
        "my_user": my_user,
        "my_pass": my_pass,
        "my_url": my_url,
        "my_user_element_id": my_user_element_id,
        "my_pass_element_id": my_pass_element_id,
        "my_button_element_id": my_button_element_id
    }
    built_shortcut = _build_shortcut(
        shortcut_string=js_login,
        my_variables=my_vars,
        debug=debug)
    print built_shortcut

def shortcut_amazon_lambda(my_values_dict, debug=False):
    my_vars = {"my_values_dict": ','.join('"{0}":"{1}"'.format(key,val) for key, val in my_values_dict.iteritems())}
    built_shortcut = _build_shortcut(
        shortcut_string=js_amazon_lamba,
        my_variables=my_vars,
        debug=debug)
    print built_shortcut
    