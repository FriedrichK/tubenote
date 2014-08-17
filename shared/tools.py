def request_has_required_parameters(request, required_parameters, method="GET"):
    missing_parameters = []

    for required_parameter in required_parameters:
        if not required_parameter in getattr(request, method):
            missing_parameters.append(required_parameter)

    if len(missing_parameters) > 0:
        return False, missing_parameters

    return True, missing_parameters
