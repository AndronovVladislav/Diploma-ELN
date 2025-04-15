import { useToast } from 'primevue/usetoast';
import { ToastServiceMethods } from 'primevue';

interface NotificationParams {
    summary?: string,
    detail: string,
    life?: number
}

class Notifier {
    private static toast: ToastServiceMethods;

    static init() {
        if (!Notifier.toast) {
            Notifier.toast = useToast();
        }
    }

    static success({ summary = 'Выполнено', detail, life = 2000 }: NotificationParams) {
        Notifier.toast.add({ severity: 'success', summary: summary, detail: detail, life: life });
    }

    static error({ summary = 'Ошибка', detail, life = 4000 }: NotificationParams) {
        Notifier.toast.add({ severity: 'error', summary: summary, detail: detail, life: life });
    }

    static info({ summary = 'Информация', detail, life = 2000 }: NotificationParams) {
        Notifier.toast.add({ severity: 'info', summary: summary, detail: detail, life: life });
    }

    static warn({ summary = 'Предупреждение', detail, life = 3000 }: NotificationParams) {
        Notifier.toast.add({ severity: 'warn', summary: summary, detail: detail, life: life });
    }
}

export function useNotifier() {
    Notifier.init();
    return Notifier;
}
