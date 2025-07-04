from flask import Flask, render_template, request
app = Flask(__name__)

def convert_unit(value, unit_from, unit_to):
    if unit_from == unit_to:
        return value
    return value / 25.4 if unit_from == "mm" and unit_to == "inch" else value * 25.4

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        try:
            mode = request.form.get("mode")
            unit = request.form.get("unit")
            decimals = int(request.form.get("decimals", 3))
            result['mode'] = mode
            result['unit'] = unit
            result['decimals'] = decimals
            unit_to = "inch" if unit == "mm" else "mm"
            result['target_unit'] = unit_to

            nominal = request.form.get("nominal")
            if nominal.strip() == "":
                raise ValueError("Thiếu giá trị danh nghĩa")
            nominal = float(nominal)

            # Xử lý dung sai
            if mode == 'symmetric':
                tolerance = request.form.get("tolerance")
                if tolerance.strip() == "":
                    raise ValueError("Thiếu giá trị dung sai")
                tolerance = float(tolerance)
                min_val = nominal - tolerance
                max_val = nominal + tolerance
                result.update({
                    "nominal": nominal,
                    "tolerance": tolerance,
                    "min_val": min_val,
                    "max_val": max_val,
                    "nominal_converted": convert_unit(nominal, unit, unit_to),
                    "symmetric_tolerance": convert_unit(tolerance, unit, unit_to),
                    "min_converted": convert_unit(min_val, unit, unit_to),
                    "max_converted": convert_unit(max_val, unit, unit_to)
                })

            elif mode == 'asymmetric':
                tol_plus = request.form.get("tol_plus")
                tol_minus = request.form.get("tol_minus")
                if tol_plus.strip() == "" or tol_minus.strip() == "":
                    raise ValueError("Thiếu dung sai + hoặc -")
                tol_plus = float(tol_plus)
                tol_minus = float(tol_minus)
                min_val = nominal - tol_minus
                max_val = nominal + tol_plus
                # Danh nghĩa đối xứng = trung bình Max Min
                nominal_avg = (max_val + min_val) / 2
                tol_avg = (max_val - min_val) / 2
                result.update({
                    "nominal": nominal,
                    "tol_plus": tol_plus,
                    "tol_minus": tol_minus,
                    "min_val": min_val,
                    "max_val": max_val,
                    "nominal_converted": convert_unit(nominal_avg, unit, unit_to),
                    "symmetric_tolerance": convert_unit(tol_avg, unit, unit_to),
                    "min_converted": convert_unit(min_val, unit, unit_to),
                    "max_converted": convert_unit(max_val, unit, unit_to)
                })

            # Xử lý đối chiếu tay nếu có
            verify_nominal = request.form.get("verify_nominal", "").strip()
            verify_tolerance = request.form.get("verify_tolerance", "").strip()

            if verify_nominal and verify_tolerance:
                v_nom = float(verify_nominal)
                v_tol = float(verify_tolerance)
                v_min = v_nom - v_tol
                v_max = v_nom + v_tol
                # quy đổi về đơn vị gốc để so sánh
                v_min_conv = convert_unit(v_min, unit_to, unit)
                v_max_conv = convert_unit(v_max, unit_to, unit)

                result.update({
                    "verify_nominal": v_nom,
                    "verify_tolerance": v_tol,
                    "verify_min_converted": v_min_conv,
                    "verify_max_converted": v_max_conv
                })

                valid = (v_min_conv >= min_val) and (v_max_conv <= max_val)
                result["verification_color"] = "green" if valid else "red"
                result["verification_result"] = "✅ Hợp lệ" if valid else "❌ Không hợp lệ"
        except Exception as e:
            result["error"] = str(e)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request
app = Flask(__name__)

def convert_unit(value, unit_from, unit_to):
    if unit_from == unit_to:
        return value
    return value / 25.4 if unit_from == "mm" and unit_to == "inch" else value * 25.4

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        try:
            mode = request.form.get("mode")
            unit = request.form.get("unit")
            decimals = int(request.form.get("decimals", 3))
            result['mode'] = mode
            result['unit'] = unit
            result['decimals'] = decimals
            unit_to = "inch" if unit == "mm" else "mm"
            result['target_unit'] = unit_to

            nominal = request.form.get("nominal")
            if nominal.strip() == "":
                raise ValueError("Thiếu giá trị danh nghĩa")
            nominal = float(nominal)

            # Xử lý dung sai
            if mode == 'symmetric':
                tolerance = request.form.get("tolerance")
                if tolerance.strip() == "":
                    raise ValueError("Thiếu giá trị dung sai")
                tolerance = float(tolerance)
                min_val = nominal - tolerance
                max_val = nominal + tolerance
                result.update({
                    "nominal": nominal,
                    "tolerance": tolerance,
                    "min_val": min_val,
                    "max_val": max_val,
                    "nominal_converted": convert_unit(nominal, unit, unit_to),
                    "symmetric_tolerance": convert_unit(tolerance, unit, unit_to),
                    "min_converted": convert_unit(min_val, unit, unit_to),
                    "max_converted": convert_unit(max_val, unit, unit_to)
                })

            elif mode == 'asymmetric':
                tol_plus = request.form.get("tol_plus")
                tol_minus = request.form.get("tol_minus")
                if tol_plus.strip() == "" or tol_minus.strip() == "":
                    raise ValueError("Thiếu dung sai + hoặc -")
                tol_plus = float(tol_plus)
                tol_minus = float(tol_minus)
                min_val = nominal - tol_minus
                max_val = nominal + tol_plus
                # Danh nghĩa đối xứng = trung bình Max Min
                nominal_avg = (max_val + min_val) / 2
                tol_avg = (max_val - min_val) / 2
                result.update({
                    "nominal": nominal,
                    "tol_plus": tol_plus,
                    "tol_minus": tol_minus,
                    "min_val": min_val,
                    "max_val": max_val,
                    "nominal_converted": convert_unit(nominal_avg, unit, unit_to),
                    "symmetric_tolerance": convert_unit(tol_avg, unit, unit_to),
                    "min_converted": convert_unit(min_val, unit, unit_to),
                    "max_converted": convert_unit(max_val, unit, unit_to)
                })

            # Xử lý đối chiếu tay nếu có
            verify_nominal = request.form.get("verify_nominal", "").strip()
            verify_tolerance = request.form.get("verify_tolerance", "").strip()

            if verify_nominal and verify_tolerance:
                v_nom = float(verify_nominal)
                v_tol = float(verify_tolerance)
                v_min = v_nom - v_tol
                v_max = v_nom + v_tol
                # quy đổi về đơn vị gốc để so sánh
                v_min_conv = convert_unit(v_min, unit_to, unit)
                v_max_conv = convert_unit(v_max, unit_to, unit)

                result.update({
                    "verify_nominal": v_nom,
                    "verify_tolerance": v_tol,
                    "verify_min_converted": v_min_conv,
                    "verify_max_converted": v_max_conv
                })

                valid = (v_min_conv >= min_val) and (v_max_conv <= max_val)
                result["verification_color"] = "green" if valid else "red"
                result["verification_result"] = "✅ Hợp lệ" if valid else "❌ Không hợp lệ"
        except Exception as e:
            result["error"] = str(e)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
b025451520eb1ec0c7590c33f0bbaa23ab6650df
