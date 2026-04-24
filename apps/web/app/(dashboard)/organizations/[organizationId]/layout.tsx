import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default async function OrganizationLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ organizationId: string }>;
}) {
  const { organizationId } = await params;
  return (
    <div className="min-h-screen bg-grid">
      <div className="sticky top-0 z-10 border-b border-slate-800 bg-slate-950/65 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-4">
          <div className="flex items-center gap-3">
            <Link href="/organizations" className="text-sm text-slate-300 hover:text-white">
              ← Организации
            </Link>
            <div className="hidden text-sm text-slate-500 md:block">BuildLaw AI</div>
          </div>
          <div className="flex items-center gap-2">
            <Button href={`/organizations/${organizationId}/documents`} variant="ghost">
              Документы
            </Button>
            <Button href={`/organizations/${organizationId}/documents/upload`} variant="primary">
              Загрузить
            </Button>
          </div>
        </div>
      </div>
      <div className="mx-auto max-w-6xl px-6 py-10">{children}</div>
    </div>
  );
}

