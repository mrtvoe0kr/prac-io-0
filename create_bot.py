
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
import io
import sympy as sp

# Инициализация глобальных переменных
current_figure = None

def reset_figure():
    global current_figure
    current_figure = plt.figure()

reset_figure()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "main_menu"
    await update.message.reply_text(
        "/menu\n"
        "1. Построение 2D графиков\n"
        "2. Построение 3D графиков\n"
        "3. Выход\n"
        "Введите номер опции, Например, 1"
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    current_state = context.user_data.get("state", "main_menu")

    if current_state == "main_menu":
        if user_input == "1":
            context.user_data["state"] = "2d_menu"
            await send_2d_menu(update, context)
        elif user_input == "2":
            context.user_data["state"] = "3d_menu"
            await send_3d_menu(update, context)
        elif user_input == "3":
            await update.message.reply_text("Выход. До свидания!")
            context.user_data.clear()
        else:
            await update.message.reply_text("Некорректная команда. Используйте /menu.")
    elif current_state == "2d_menu":
        if user_input == "1.1":
            context.user_data["state"] = "2d_explicit"
            await update.message.reply_text("Введите функцию в формате 'y = выражение'. Например, 'y = x^2'.")
        elif user_input == "1.2":
            context.user_data["state"] = "2d_implicit"
            await update.message.reply_text("Введите уравнение в формате 'выражение = выражение'. Например, 'x^2 + y^2 = 1'.")
        elif user_input == "1.3":
            context.user_data["state"] = "2d_parametric"
            await update.message.reply_text(
                "Введите параметрическую функцию в формате:\n"
                "'x = выражение, y = выражение, t_min = значение, t_max = значение'.\n"
                "Например: 'x = sin(t), y = cos(t), t_min = 0, t_max = 2*pi'."
            )
        elif user_input == "1.4":
            reset_figure()
            await update.message.reply_text("2D график очищен.")
        elif user_input == "1.5":
            context.user_data["state"] = "main_menu"
            await start(update, context)
        else:
            await update.message.reply_text("Некорректная команда. Выберите пункт из меню 2D.")
    elif current_state == "2d_explicit":
        await draw_explicit_2D(update, context)
        context.user_data["state"] = "2d_menu"
    elif current_state == "2d_implicit":
        await draw_implicit_2D(update, context)
        context.user_data["state"] = "2d_menu"
    elif current_state == "2d_parametric":
        await draw_parametric_2D(update, context)
        context.user_data["state"] = "2d_menu"
    elif current_state == "3d_menu":
        if user_input == "2.1":
            context.user_data["state"] = "3d_surface"
            await update.message.reply_text("Введите функцию в формате 'z = выражение'. Например, 'z = 4 - x^2'.")
        elif user_input == "2.2":
            context.user_data["state"] = "3d_parametric"
            await update.message.reply_text(
                "Введите параметрическую поверхность в формате:\n"
                "'x = выражение, y = выражение, z = выражение, "
                "u_min = значение, u_max = значение, v_min = значение, v_max = значение'."
            )
        elif user_input == "2.3":
            reset_figure()
            await update.message.reply_text("3D график очищен.")
        elif user_input == "2.4":
            context.user_data["state"] = "main_menu"
            await start(update, context)
        else:
            await update.message.reply_text("Некорректная команда. Выберите пункт из меню 3D.")
    elif current_state == "3d_surface":
        await draw_surface_3D(update, context)
    elif current_state == "3d_parametric":
        await draw_parametric_surface_3D(update, context)
    else:
        await update.message.reply_text("Ошибка состояния. Используйте /menu для возврата в главное меню.")
        context.user_data["state"] = "main_menu"

async def send_2d_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Меню 2D графиков:\n"
        "1.1 Нарисовать явную функцию\n"
        "1.2 Нарисовать неявную функцию\n"
        "1.3 Нарисовать параметрическую функцию\n"
        "1.4. Очистить график\n"
        "1.5 Назад в главное меню\n"
        "Введите номер опции, Например, 1.1"
    )

async def handle_2d_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    current_state = context.user_data.get("state", "2d_menu")

    if current_state == "2d_menu":
        if user_input == "1.2":
            context.user_data["state"] = "2d_explicit"
            await update.message.reply_text("Введите функцию в формате 'y = выражение'. Например, 'y = x^2'.")
        elif user_input == "1.2":
            context.user_data["state"] = "2d_implicit"
            await update.message.reply_text("Введите уравнение в формате 'выражение = выражение'. Например, 'x^2 + y^2 = 1'.")
        elif user_input == "1.3":
            context.user_data["state"] = "2d_parametric"
            await update.message.reply_text(
                "Введите параметрическую функцию в формате:\n"
                "'x = выражение, y = выражение, t_min = значение, t_max = значение'."
                "\nНапример: 'x = sin(t), y = cos(t), t_min = 0, t_max = 2*pi'."
            )
        elif user_input == "1.4":
            reset_figure()
            await update.message.reply_text("2D график очищен.")
        elif user_input == "1.5":
            context.user_data["state"] = "main_menu"
            await start(update, context)
        else:
            await update.message.reply_text("Некорректная команда. Выберите пункт из меню 2D.")
    elif current_state == "2d_explicit":
        await draw_explicit_2D(update, context)
        context.user_data["state"] = "2d_menu"
    elif current_state == "2d_implicit":
        await draw_implicit_2D(update, context)
        context.user_data["state"] = "2d_menu"
    elif current_state == "2d_parametric":
        await draw_parametric_2D(update, context)
        context.user_data["state"] = "2d_menu"
    else:
        await update.message.reply_text("Ошибка состояния")
        context.user_data["state"] = "2d_menu"

async def send_3d_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Меню 3D графиков:\n"
        "2.1 Нарисовать поверхность\n"
        "2.2 Нарисовать параметрическую поверхность\n"
        "2.3 Очистить график\n"
        "2.4 Назад в главное меню\n"
        "Введите номер опции, Например, 2.1"
    )

async def handle_3d_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    current_state = context.user_data.get("state", "3d_menu")

    if current_state == "3d_menu":
        if user_input == "2.1":
            context.user_data["state"] = "3d_surface"
            await update.message.reply_text("Введите функцию в формате 'z = выражение'. Например, 'z = sqrt(4 - x^2)'.")
        elif user_input == "2.2":
            context.user_data["state"] = "3d_parametric"
            await update.message.reply_text(

                "Введите параметрическую поверхность в формате:\n"
                "'x = выражение, y = выражение, z = выражение, "
                "u_min = значение, u_max = значение, v_min = значение, v_max = значение'."
                "\nНапример: 'x = cos(u)*sin(v), y = sin(u)*sin(v), z = cos(v), "
                "u_min = 0, u_max = 2*pi, v_min = 0, v_max = pi'."
            )
        elif user_input == "2.3":
            reset_figure()
            await update.message.reply_text("3D график очищен.")
        elif user_input == "2.4":
            context.user_data["state"] = "main_menu"
            await start(update, context)
        else:
            await update.message.reply_text("Некорректная команда. Выберите пункт из меню 3D.")
    elif current_state == "3d_surface":
        await draw_surface_3D(update, context)
        context.user_data["state"] = "3d_menu"
    elif current_state == "3d_parametric":
        await draw_parametric_surface_3D(update, context)
        context.user_data["state"] = "3d_menu"

############################################################################
############################################################################
def update_legend(ax, label, color):
    handles, labels = ax.get_legend_handles_labels()

    # Проверяем, существует ли уже такая подпись
    if label not in labels:
        proxy = plt.Line2D([0], [0], color=color, lw=2)  # Прокси-объект для легенды
        handles.append(proxy)
        labels.append(label)

    ax.legend(handles, labels, loc='upper right')

# Инициализация палитры цветов
color_palette = list(cm.tab10.colors)  # используем палитру из 10 цветов
color_cycle = cycler(color=color_palette)
current_color_index = 0
# Глобальный список для хранения информации о графиках
plot_handles = []
plot_labels = []
##############################################################################
async def draw_explicit_2D(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_color_index
    try:
        func_input = update.message.text.strip()

        if not func_input.lower().startswith('y='):
            await update.message.reply_text("Некорректный ввод. Используйте формат 'y = выражение'.")
            return

        func = func_input[2:].strip().replace('^', '**')
        x = np.linspace(-10, 10, 400)
        env = {"x": x, "np": np, "sqrt": np.sqrt, "cos": np.cos, "sin": np.sin, "ln": np.log}
        y = eval(func, env)

        if current_figure is None:
            reset_figure()

        ax = current_figure.gca()

        color = color_palette[current_color_index % len(color_palette)]
        current_color_index += 1

        ax.plot(x, y, label=func_input, color=color)
        update_legend(ax, func_input, color)

        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        ax.grid(True)

        await send_plot(update, context)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def draw_implicit_2D(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_color_index
    try:
        equation_input = update.message.text.strip()

        if "=" not in equation_input:
            await update.message.reply_text("Некорректный ввод. Используйте формат 'выражение = выражение'.")
            return

        left, right = map(str.strip, equation_input.split('='))
        x, y = sp.symbols('x y')
        diff_expr = sp.sympify(left.replace('^', '**')) - sp.sympify(right.replace('^', '**'))

        x_vals = np.linspace(-10, 10, 400)
        y_vals = np.linspace(-10, 10, 400)
        X, Y = np.meshgrid(x_vals, y_vals)

        func = sp.lambdify((x, y), diff_expr, 'numpy')
        Z = func(X, Y)

        if current_figure is None:
            reset_figure()

        ax = current_figure.gca()

        color = color_palette[current_color_index % len(color_palette)]
        current_color_index += 1

        ax.contour(X, Y, Z, levels=[0], colors=[color])
        update_legend(ax, f"{left} = {right}", color)

        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        ax.grid(True)

        await send_plot(update, context)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def draw_parametric_2D(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_color_index
    try:
        func_input = update.message.text.strip().replace(" ", "")

        if not all(keyword in func_input for keyword in ["x=", "y=", "t_min=", "t_max="]):
            await update.message.reply_text(
                "Некорректный ввод. Используйте формат:\n"
                "'x = выражение, y = выражение, t_min = значение, t_max = значение'."
            )
            return

        parts = [part.strip() for part in func_input.split(',')]
        x_expr = parts[0].split('=')[1]
        y_expr = parts[1].split('=')[1]
        t_min = float(sp.sympify(parts[2].split('=')[1]))
        t_max = float(sp.sympify(parts[3].split('=')[1]))

        t = np.linspace(t_min, t_max, 400)
        env = {"t": t, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "pi": np.pi}

        x = eval(x_expr.replace('^', '**'), env)
        y = eval(y_expr.replace('^', '**'), env)

        if current_figure is None:
            reset_figure()

        ax = current_figure.gca()

        color = color_palette[current_color_index % len(color_palette)]
        current_color_index += 1

        ax.plot(x, y, label=func_input, color=color)
        update_legend(ax, func_input, color)

        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        ax.grid(True)

        await send_plot(update, context)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
        
async def draw_surface_3D(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # получаем пользовательский ввод
        func_input = update.message.text.strip()

        if not func_input.startswith('z='):
            await update.message.reply_text("Некорректный ввод. Используйте формат 'z = выражение'.")
            return

        func = func_input[2:].strip().replace('^', '**')

        # Создаём сетку значений
        x_vals = np.linspace(-10, 10, 100)
        y_vals = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x_vals, y_vals)
        env = {"x": X, "y": Y, "np": np, "sqrt": np.sqrt}

        Z = eval(func, env)

        # сбрасываем график
        if current_figure is None:
            reset_figure()

        ax = current_figure.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Отправляем график
        await send_plot(update, context)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def draw_parametric_surface_3D(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # получаем пользовательский ввод и убираем пробелы вокруг запятых
        func_input = update.message.text.strip().replace(" ", "")
        
        # Проверяем, что все параметры присутствуют
        if not all(keyword in func_input for keyword in ["x=", "y=", "z=", "u_min=", "u_max=", "v_min=", "v_max="]):
            await update.message.reply_text(
                "Некорректный ввод. Используйте формат:\n"
                "'x = выражение, y = выражение, z = выражение, "
                "u_min = значение, u_max = значение, v_min = значение, v_max = значение'."
            )
            return

        # Разделяем параметры
        parts = [part.strip() for part in func_input.split(',')]
        if len(parts) != 7:
            await update.message.reply_text(
                "Некорректный ввод. Убедитесь, что указаны все параметры: x, y, z, u_min, u_max, v_min и v_max."
            )
            return

        x_expr = parts[0].split('=')[1].strip()
        y_expr = parts[1].split('=')[1].strip()
        z_expr = parts[2].split('=')[1].strip()
        u_min = float(sp.sympify(parts[3].split('=')[1].strip()))
        u_max = float(sp.sympify(parts[4].split('=')[1].strip()))
        v_min = float(sp.sympify(parts[5].split('=')[1].strip()))
        v_max = float(sp.sympify(parts[6].split('=')[1].strip()))

        # Генерация значений параметров u и v
        u = np.linspace(u_min, u_max, 100)
        v = np.linspace(v_min, v_max, 100)
        U, V = np.meshgrid(u, v)
        env = {"u": U, "v": V, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "pi": np.pi, "sqrt": np.sqrt, "cos": np.cos, "sin": np.sin, "ln": np.log}

        X = eval(x_expr.replace('^', '**'), env)
        Y = eval(y_expr.replace('^', '**'), env)
        Z = eval(z_expr.replace('^', '**'), env)

        # Сбрасываем график
        if current_figure is None:
            reset_figure()

        ax = current_figure.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Отправляем график
        await send_plot(update, context)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

############################################################################

async def send_plot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    await update.message.reply_photo(buf)
    buf.close()

async def clear_plot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_figure()
    await update.message.reply_text("График очищен.")

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'clear_2D' or query.data == 'clear_3D':
        reset_figure()
        await query.edit_message_text("Plot cleared.")
    else:
        await query.edit_message_text(f"Selected: {query.data}")

############################################################################
############################################################################

def main():
    application = Application.builder().token("7576284019:AAGD2OhRgmwABgghXLkEgLB7-t-W-YHouaU").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('menu', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    application.run_polling()

if __name__ == '__main__':
    main()
